import psutil, os

#print(psutil.cpu_times_percent())
#print(psutil.cpu_times_percent())
#print(psutil.cpu_times_percent().system)
#print(psutil.cpu_times_percent().idle)
#print(psutil.cpu_times_percent().interrupt)
#print(psutil.cpu_times_percent().dpc)

#print(psutil.cpu_count())#grafik çıkmaz
#print(psutil.boot_time())#grafik çıkmaz
#print(psutil.disk_partitions())#grafik çıkmaz

#print(psutil.disk_io_counters())#grafik çıkar
#print(psutil.disk_usage(os.getcwd())) # garfik çıkar doughnut
#tamamlananlar üst kısımda



print(psutil.cpu_stats())#grafik çıkar

#print(psutil.net_io_counters()) # garfik çıkar






