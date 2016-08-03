# Check java
if type -p java > /dev/null; then
  _java=java
else
  echo "Java was not installed or is not on your PATH."
  exit -100;
fi

if [[ "$_java" ]]; then
  version=$("$_java" -version 2>&1 | awk -F '"' '/version/ {print $2}')
  if [[ "$version" < "1.8" ]]; then
    echo "Dockstore requires Java version 1.8 and above."
    exit -100;
  else
    echo "The java version $version"
  fi
fi

# Check Existence Python
if type -p python > /dev/null; then
  _python=python
else
  echo "python was not installed or is not on your PATH."
  exit -100;
fi
# Check the python version
if [[ "$_python" ]]; then
  version=$("$_python" --version 2>&1 | awk '{print $2}')
  if [[ "$version" < "2.7" ]]; then
    echo "Dockstore requires Java version 1.8 and above."
    # exit -100;
  else
    echo "Python version is $version"
  fi
fi

#Check Docker
if type -p docker > /dev/null; then
  _docker=docker
else
  echo "docker was not installed or is not on your PATH."
  exit -100;
fi

if [[ "$_docker" ]]; then
  docker_version=$("$_docker" --version 2>&1 | awk '{print $3}')
  docker_version=${docker_version::-1}
  if [[ "$version" < "1.0" ]]; then
    echo "Dockstore requires docker version 1.1 and above."
    exit -100;
  else
    echo " version is $docker_version"
  fi
fi
