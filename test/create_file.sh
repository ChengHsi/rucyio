TEMP_DIR=/root/chchao/rucyio/tmp
now=$(date +"%Y%m%dT%H%M%S")
TESTFILE=$TEMP_DIR/file$now

dd if=/dev/random bs=512 count=1 of=$TESTFILE
echo "Created dummy file: $TESTFILE"
echo "Set to Alias \$TESTFILE"
export TESTFILE=$TESTFILE
# rucio upload --scope ams-user-chenghsi --rse EOS00_AMS02SCRATCHDISK $filepath
