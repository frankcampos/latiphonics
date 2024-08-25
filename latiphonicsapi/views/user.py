from latiphonicsapi.models import User
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

@api_view(['POST', 'PUT'])
def check_user(request):
    '''Checks to see if User has Associated Gamer

    Method arguments:
      request -- The full HTTP request object
    '''
    uid = request.data['uid']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    user = User.objects.filter(uid=uid).first()

    # If authentication was successful, respond with their token
    if user is not None:
        data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'photo': user.photo,
            'about': user.about,
            'uid': user.uid,
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = {'valid': False}
        return Response(data)

@api_view(['POST'])
def register_user(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Now save the user info in the levelupapi_gamer table
    user = User.objects.create(
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        photo=request.data['photo'],
        about=request.data['about'],
        uid=request.data['uid']
    )

    # Return the gamer info to the client
    data = {
        'id': user.id,
        'uid': user.uid,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'photo': user.photo,
        'about': user.about
    }
    return Response(data)

@api_view(['DELETE'])
def delete_user(request):
    try:
        user_id = request.data['user_id']
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

@api_view(['GET'])
def get_user(request):
    try:
        user_id = request.query_params.get('user_id')
        user = User.objects.get(id=user_id)
        data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'photo': user.photo,
            'about': user.about,
            'uid': user.uid
        }
        return Response(data)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

@api_view(['put'])
def update_user(request):
    try:
        user_id = request.data['user_id']
        user = User.objects.get(id=user_id)
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.photo = request.data['photo']
        user.about = request.data['about']
        user.save()
        data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'photo': user.photo,
            'about': user.about,
            'uid': user.uid

        }
        return Response(data)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
