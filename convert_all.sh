#!/usr/bin/env bash
cd /media/data_1/home/zelin/vrtmp/
root_dir=/media/data_1/home/zelin/vrtmp/
name=Junliu
shapes_in_dir=${root_dir}input/${name}/initial
shapes_out_dir=${root_dir}output/${name}
mkdir -p $shapes_out_dir
shapes_out_dir=${root_dir}output/${name}/initial
mkdir -p $shapes_out_dir
echo $shapes_in_dir
cd $shapes_in_dir
for i in $( ls );
do
	echo Handling $i
	j=`basename $i .stl`
	meshlabserver -i $shapes_in_dir"/"$i -o $shapes_out_dir"/"$j.obj
done

shapes_out_dir=${root_dir}output/${name}/final
mkdir -p $shapes_out_dir
shapes_in_dir=${root_dir}input/${name}/final
echo $shapes_in_dir
cd $shapes_in_dir
for i in $( ls );
do
	echo Handling $i
	j=`basename $i .stl`
	meshlabserver -i $shapes_in_dir"/"$i -o $shapes_out_dir"/"$j.obj
done
#
#for i in $( find -maxdepth 1 -type d );
#do
#	echo Handling echo ${i:2}
#done