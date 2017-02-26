CURDIR=`pwd` 

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASEDIR=`dirname $SCRIPTDIR`

echo "Main directory: $BASEDIR"

echo "Going to script directory: $SCRIPTDIR"
cd $SCRIPTDIR

echo "Building image"
docker build -t pas:latest .

echo "Removing container if exists"
docker rm -f pas || echo "Container does not exist"

echo "Creating container"
docker run -d --name pas -v $BASEDIR:/opt/pas pas:latest 

echo "Going back to $CURDIR"
cd $CURDIR