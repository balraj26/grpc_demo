# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import time


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message="Hello, %s!" % request.name)

    def SayHelloStreamServer(self, request, context):
        requests_number = int(input("Enter number of designations:\n"))
        for _ in range(requests_number):
            designation = input("Enter the designation\n")
            yield helloworld_pb2.HelloReply(message=f"Hello, {request.name} designation {designation}!")

    def SayHelloStreamClient(self, request_iterator, context):
        name = []
        for request in request_iterator:
            name.append(request.name)
        return helloworld_pb2.HelloReply(message=f"Hello to you all {name}")

    def SayHelloBidiStream(self, request_iterator, context):
        i = 0
        for request in request_iterator:
            profession = input(f"Enter the profession of {request.name}:\n")
            message = f"Hello {request.name} the {profession}"
            yield helloworld_pb2.HelloReply(message=message)


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
