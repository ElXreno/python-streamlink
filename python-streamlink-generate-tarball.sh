#!/bin/bash

VERSION=$1
SHORT_VERSION=$VERSION
[[ "$VERSION" =~ [a-f0-9]{7,} ]] && SHORT_VERSION=${VERSION:0:7}

SRC_TARBALL=streamlink-$SHORT_VERSION.tar.gz
DEST_TARBALL=streamlink-$SHORT_VERSION-without-win32-binaries.tar.gz

curl -L -R -O https://github.com/streamlink/streamlink/archive/$SHORT_VERSION/$SRC_TARBALL
gunzip <$SRC_TARBALL | tar --delete streamlink-$VERSION/win32 | gzip >$DEST_TARBALL
rm $SRC_TARBALL
