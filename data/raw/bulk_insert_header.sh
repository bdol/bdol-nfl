for i in *games.tsv
do
  #cat schedule_headers.tsv $i >$i.new
  cat schedule_headers.tsv $i >$i.new && mv $i.new $i
done
