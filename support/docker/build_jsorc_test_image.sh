docker build -t jsorc-test-image:latest     --build-arg JASECI_PYPI_VERSION=1.3.6.3     --build-arg JASECI_SERV_PYPI_VERSION=1.3.6.3     --build-arg JASECI_AI_KIT_PYPI_VERSION=1.3.6.3     --build-arg BUILD_WITH_AI=1 -f jaseci.Dockerfile ../../