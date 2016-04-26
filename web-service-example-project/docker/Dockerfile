#
# Copyright 2016 The Open Source Research Group,
#                University of Erlangen-Nürnberg
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
#
FROM osrgroup/amos-web-service-base-image:1.0

ENV JETTY_RUNNER_VERSION 9.3.8.v20160314
ENV MAVEN_DOWNLOAD_URL http://search.maven.org/remotecontent?filepath=

RUN mkdir -p /usr/share/java \
  && wget "${MAVEN_DOWNLOAD_URL}org/eclipse/jetty/jetty-runner/${JETTY_RUNNER_VERSION}/jetty-runner-${JETTY_RUNNER_VERSION}.jar" \
        -O /usr/share/java/jetty-runner-${JETTY_RUNNER_VERSION}.jar \
  && ln -s /usr/share/java/jetty-runner-${JETTY_RUNNER_VERSION}.jar /usr/share/java/jetty-runner.jar

ADD assets/ /web-service-assets

RUN bash /web-service-assets/finish_docker_build
