SRC_DIR=$1
DST_DIR=$2

CROP_PERCENT=75

DEBUG=true

function usage() {
    echo 'Usage: crop-dataset_CASIA-maxpy-clean.sh SOURCE_DIR DESTINATION_DIR'
}


function copy_file() {
    echo "Copying file to destination directory ..."
    DIR_LIST=`ls $SRC_DIR`
    for d in $DIR_LIST; do
        FILE_LIST=`ls $SRC_DIR/$d`
        FILE_NUM=`ls $SRC_DIR/$d | wc -l`
        COPY_FILE_NUM=`expr $FILE_NUM - $FILE_NUM \* $CROP_PERCENT / 100`

        if [ $COPY_FILE_NUM -eq 0 ]; then
            continue
        fi

        # Create target directory if it does not exist
        if [ ! -d $DST_DIR/$d ]; then
            mkdir $DST_DIR/$d
        else
            rm -rf $DST_DIR/$d/*
        fi

        # Copy file from source directory to target directory
        i=1
        for f in $FILE_LIST; do
            if $DEBUG; then
                echo "Copy $f from $SRC_DIR/$d to $DST_DIR/$d"
            else
                echo -n '.'
            fi
            cp $SRC_DIR/$d/$f $DST_DIR/$d/
            i=`expr $i + 1`
            if [ $i -gt $COPY_FILE_NUM ]; then
                break
            fi
        done

        # break
    done
}


if [ -z $SRC_DIR ]; then
    usage
    exit
fi

if [ -z $DST_DIR ]; then
    usage
    exit
fi

copy_file
