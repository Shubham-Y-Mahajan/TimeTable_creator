from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CourseData
from .serializers import CourseSerializer
from .backend import process_submission
import random
import requests
@api_view(['GET'])
def get_all_courses(request):
    courses = CourseData.objects.all()  # Fetch all courses
    serializer = CourseSerializer(courses, many=True)  # Serialize the data
    return Response(serializer.data)  # Return JSON response

@api_view(['POST'])
def submit_selection(request):
    data = request.data

    # Validate that 'course_id_list' is in the request and is a list of integers
    if 'course_id_list' not in data or not isinstance(data['course_id_list'], list):
        return Response({'error': 'course_id_list must be provided as a list.'}, status=status.HTTP_400_BAD_REQUEST)

    # Optional: Check if all items in the list are integers
    if not all(isinstance(item, int) for item in data['course_id_list']):
        return Response({'error': 'All items in course_id_list must be integers.'}, status=status.HTTP_400_BAD_REQUEST)

    content = process_submission(data['course_id_list'])
    if type(content) == int:
        return Response({'error': f'Course with id {content} does not exist'}, status=status.HTTP_404_NOT_FOUND)

    else:
        grid_map, clashes, additional_messages = content
        return Response({'mapping': grid_map,'clashes':clashes,'additional_messages':additional_messages}, status=status.HTTP_200_OK)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/116.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 10; Mobile; rv:79.0) Gecko/79.0 Firefox/79.0",
]

@api_view(["GET"])
def real_user_ping(request):
    """
        used to call student forum's api to prevent circular calling
        (calling request on your own instance causes deadlock)
    """
    try:
        chosen_ua = random.choice(USER_AGENTS)
        target_url = f"https://iit-bhilai-student-forum.onrender.com/get_analytics/"

        headers = {
            "User-Agent": chosen_ua
        }

        internal_response = requests.get(target_url, headers=headers)

        return Response({
            "message": "Pinged /get_analytics/ as a browser",
            "target_url": target_url,
            "user_agent_used": chosen_ua,
            "status_code": internal_response.status_code,
            "internal_response": internal_response
        })

    except Exception as e:
        return Response({
            "message": "Ping failed",
            "error": str(e)
        }, status=500)