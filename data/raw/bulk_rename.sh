for files in *_.tsv
do
 mv "$files" "${files%_.tsv}.tsv"
done
