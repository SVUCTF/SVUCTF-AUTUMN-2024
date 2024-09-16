import os
import uuid
from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection

import user_info_v2_pb2
import user_info_v2_pb2_grpc
import user_info_v1_pb2
import user_info_v1_pb2_grpc
import flag_pb2
import flag_pb2_grpc

FLAG = os.environ.get("GZCTF_FLAG", "SVUCTF{test_flag}")


class UserInfoServiceV2(user_info_v2_pb2_grpc.UserInfoServiceV2Servicer):
    def __init__(self, users):
        self.users = users

    def GetUserInfo(self, request, context):
        user = self.users.get(request.user_id)
        if user:
            response = user_info_v2_pb2.UserInfoResponseV2(
                user_id=user["user_id"],
                username=user["username"],
                email=user["email"],
                role=user["role"],
            )
            context.set_trailing_metadata(
                (
                    (
                        "note",
                        "This version has been updated for security reasons and no longer returns sensitive information like auth tokens.",
                    ),
                )
            )
            return response

        context.abort(grpc.StatusCode.NOT_FOUND, "User not found")


class UserInfoServiceV1(user_info_v1_pb2_grpc.UserInfoServiceV1Servicer):
    def __init__(self, users):
        self.users = users

    def GetUserInfo(self, request, context):
        user = self.users.get(request.user_id)
        if user:
            return user_info_v1_pb2.UserInfoResponseV1(
                user_id=user["user_id"],
                username=user["username"],
                email=user["email"],
                role=user["role"],
                auth_token=user["auth_token"],
            )

        context.abort(grpc.StatusCode.NOT_FOUND, "User not found")


class FlagService(flag_pb2_grpc.FlagServiceServicer):
    def __init__(self, users):
        self.users = users

    def GetFlag(self, request, context):
        token = request.token
        user = next((u for u in self.users.values() if u["auth_token"] == token), None)

        if user and user["role"] == "admin":
            return flag_pb2.FlagResponse(flag=FLAG)

        context.abort(
            grpc.StatusCode.PERMISSION_DENIED,
            "Access denied. Invalid token or insufficient permissions.",
        )


def serve():
    users = {
        0: {
            "user_id": 0,
            "username": "admin",
            "email": "admin@company.internal",
            "role": "admin",
            "auth_token": str(uuid.uuid4()),
        },
        1: {
            "user_id": 1,
            "username": "13m0n4de",
            "email": "13m0n4de@svuctf.com",
            "role": "user",
            "auth_token": str(uuid.uuid4()),
        },
        2: {
            "user_id": 2,
            "username": "johndoe",
            "email": "johndoe@example.com",
            "role": "user",
            "auth_token": str(uuid.uuid4()),
        },
        3: {
            "user_id": 3,
            "username": "alice",
            "email": "alice@example.com",
            "role": "user",
            "auth_token": str(uuid.uuid4()),
        },
        4: {
            "user_id": 4,
            "username": "bob",
            "email": "bob@example.com",
            "role": "user",
            "auth_token": str(uuid.uuid4()),
        },
        5: {
            "user_id": 5,
            "username": "guest",
            "email": "guest@example.com",
            "role": "guest",
            "auth_token": str(uuid.uuid4()),
        },
    }

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Add services to server
    user_info_v2_pb2_grpc.add_UserInfoServiceV2Servicer_to_server(
        UserInfoServiceV2(users), server
    )
    user_info_v1_pb2_grpc.add_UserInfoServiceV1Servicer_to_server(
        UserInfoServiceV1(users), server
    )
    flag_pb2_grpc.add_FlagServiceServicer_to_server(FlagService(users), server)

    # Only add V2 and FlagService to reflection
    service_names = (
        user_info_v2_pb2.DESCRIPTOR.services_by_name["UserInfoServiceV2"].full_name,
        flag_pb2.DESCRIPTOR.services_by_name["FlagService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
