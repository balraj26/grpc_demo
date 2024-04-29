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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging

import grpc
import helloworld_pb2
import helloworld_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)

        # Single request
        response = stub.SayHello(helloworld_pb2.HelloRequest(name="Ballu"))
        print("Greeter client received:", response.message)

        # Server streaming
        response_stream = stub.SayHelloStreamReply(helloworld_pb2.HelloRequest(name='Alice'))
        for reply in response_stream:
            print("Server stream response received:", reply.message)

        # Client streaming
        names = ["Alice", "Bob", "Charlie"]
        client_stream_requests = (helloworld_pb2.HelloRequest(name=name) for name in names)
        client_stream_response = stub.SayHelloStreamRequest(client_stream_requests)
        print("Client stream response received:", client_stream_response.message)

        # Bidirectional Streaming
        # Create a stream of HelloRequest messages
        bidi_requests = (helloworld_pb2.HelloRequest(name=name) for name in ["Alice", "Bob", "Charlie"])
        # Call the SayHelloBidiStream method with the stream of requests
        bidi_response_stream = stub.SayHelloBidiStream(bidi_requests)
        # Iterate over the response stream and print each message received from the server
        for response in bidi_response_stream:
            print("Bidi stream response Received:", response.message)


if __name__ == "__main__":
    logging.basicConfig()
    run()
