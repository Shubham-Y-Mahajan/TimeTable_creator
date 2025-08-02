"use client";

import { useRouter } from "next/navigation";
import { Download, ArrowLeft } from "lucide-react";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import { timeSlots } from "@/src/lib/types";
import { days } from "@/src/lib/types";
import { useSelector } from "react-redux";
import { RootState } from "@/src/redux/store";
import { clearTimetable } from "@/src/redux/slices/timetableSlice";
import { isNotCourse } from "@/src/lib/utils";
import { useEffect, useState } from "react";
import { useDispatch } from "react-redux";

export default function Timetable() {
  const router = useRouter();
  const dispatch = useDispatch();
  const { mapping, clashes, additional_messages } = useSelector(
    (state: RootState) => state.timetable
  );

  const [isLoaded, setIsLoaded] = useState(false);
  const [downloadingPDF, setDownloadingPDF] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
    console.log("Timetable state:", { mapping, clashes, additional_messages });
  }, [mapping, clashes, additional_messages]);

  const downloadPDF = async () => {
    setDownloadingPDF(true);
    try {
      const element = document.getElementById("timetable");
      if (!element) {
        console.error("Timetable element not found");
        return;
      }

      // Create a clone of the element to modify for printing
      const printElement = element.cloneNode(true) as HTMLElement;

      // Apply basic styling to the cloned element
      printElement.style.position = "absolute";
      printElement.style.left = "-9999px";
      printElement.style.top = "-9999px";
      document.body.appendChild(printElement);

      // Override problematic styles with standard colors
      const allElements = printElement.querySelectorAll("*");
      allElements.forEach((el) => {
        const htmlEl = el as HTMLElement;
        // Replace any modern color formats with standard hex/rgb
        if (htmlEl.classList.contains("bg-blue-500")) {
          htmlEl.style.backgroundColor = "#3b82f6"; // standard hex for blue-500
        }
        // Add more replacements as needed for other tailwind classes
      });

      // Create canvas with explicit background color
      const canvas = await html2canvas(printElement, {
        backgroundColor: "#ffffff",
        useCORS: true,
        scale: 2, // Higher quality
        logging: false,
        ignoreElements: (element) => {
          // Ignore elements with modern color formats if needed
          return false;
        },
      });

      // Remove the cloned element
      document.body.removeChild(printElement);

      // Create PDF
      const imgData = canvas.toDataURL("image/png");
      const pdf = new jsPDF({
        orientation: "landscape",
        unit: "mm",
      });

      const imgWidth = 280; // slightly smaller than A4 landscape width
      const imgHeight = (canvas.height * imgWidth) / canvas.width;

      pdf.addImage(imgData, "PNG", 10, 10, imgWidth, imgHeight);
      pdf.save("timetable.pdf");
    } catch (error) {
      console.error("Error generating PDF:", error);
      alert(
        "There was an error generating the PDF. Please try again or use screenshot instead."
      );
    } finally {
      setDownloadingPDF(false);
    }
  };

  const handleBack = () => {
    dispatch(clearTimetable());
    router.back();
  };

  // Alternative screenshot method as fallback
  const downloadScreenshot = async () => {
    setDownloadingPDF(true);
    try {
      const element = document.getElementById("timetable");
      if (!element) return;

      const canvas = await html2canvas(element, {
        backgroundColor: "#ffffff",
        useCORS: true,
        scale: 2,
        onclone: (clonedDoc, element) => {
          // Find all elements with classes that might cause issues
          const blueElements = element.querySelectorAll(".bg-blue-500");

          // Apply direct inline styles instead of classes
          blueElements.forEach((el) => {
            (el as HTMLElement).style.backgroundColor = "#3b82f6";
          });
        },
      });

      // Create a download link for the image instead of PDF
      const image = canvas.toDataURL("image/png");
      const link = document.createElement("a");
      link.href = image;
      link.download = "timetable.png";
      link.click();
    } catch (error) {
      console.error("Error generating screenshot:", error);
      alert(
        "Could not generate screenshot. Please try using your device's built-in screenshot functionality."
      );
    } finally {
      setDownloadingPDF(false);
    }
  };

  if (!isLoaded || !mapping || Object.keys(mapping).length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading timetable data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <button
            onClick={handleBack}
            className="flex items-center text-gray-600 hover:text-gray-900"
          >
            <ArrowLeft className="h-5 w-5 mr-2" />
            Back
          </button>
          <div className="flex space-x-3">
            <button
              onClick={downloadPDF}
              disabled={downloadingPDF}
              className="flex items-center bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:bg-blue-300"
            >
              <Download className="h-5 w-5 mr-2" />
              {downloadingPDF ? "Processing..." : "Download PDF"}
            </button>
            <button
              onClick={downloadScreenshot}
              disabled={downloadingPDF}
              className="flex items-center bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:bg-green-300"
            >
              <Download className="h-5 w-5 mr-2" />
              Download PNG
            </button>
          </div>
        </div>

        <div id="timetable" className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-bold text-center mb-6">
            Course Timetable
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr>
                  <th className="border p-2 bg-gray-50">Day</th>
                  {timeSlots.map((slot) => (
                    <th key={slot} className="border p-2 bg-gray-50">
                      {slot}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {days.map((day, dayIndex) => (
                  <tr key={day}>
                    <td className="border p-2 font-medium">{day}</td>
                    {timeSlots.map((_, slotIndex) => {
                      const coordinate = `${dayIndex + 1}${slotIndex + 1}`;
                      const course = mapping[coordinate];

                      // Use inline styles instead of tailwind classes for PDF compatibility
                      const cellStyle =
                        course && !isNotCourse(course)
                          ? { backgroundColor: "#3b82f6", color: "white" }
                          : {};

                      return (
                        <td
                          key={`${day}-${slotIndex}`}
                          className="border p-2 text-center"
                          style={cellStyle}
                        >
                          {course && course !== "  " ? course : ""}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="mb-6">
            <h3 className="text-xl font-bold text-red-600 mb-3">
              Clash Detections
            </h3>
            {clashes && clashes.length > 0 ? (
              <ul className="list-disc pl-5 space-y-2">
                {clashes.map((message, index) => (
                  <li key={index} className="text-red-600">
                    {message}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-600">No clashes detected.</p>
            )}
          </div>

          <div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              Additional Information
            </h3>
            {additional_messages && additional_messages.length > 0 ? (
              <ul className="list-disc pl-5 space-y-2">
                {additional_messages.map((message, index) => (
                  <li key={index} className="text-gray-700">
                    {message}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-600">No additional information.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
