from Videos.admin import VideoItemRessource

dataset = VideoItemRessource().export()
file = open("backup_videos.json", "w")
file.write(dataset.json)
file.close()
exit()