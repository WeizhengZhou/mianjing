import re


FILE_NAME = 'google_design.txt'


f = open(FILE_NAME)
data = f.read()
post_list = data.split('-*' * 80)[1:]


post_by_date = {}
for post in post_list:
  publish_date = re.search(r'\d{4}-\d+-\d+', post).group()
  if not post_by_date.get(publish_date):
    post_by_date[publish_date] = []
  post_by_date[publish_date].append(post)

publish_dates = sorted(post_by_date.keys(), reverse=True)


with open(FILE_NAME, 'w+') as f:
  f.write('')

with open(FILE_NAME, 'a+') as f:
  for publish_date in publish_dates:
    for post in post_by_date[publish_date]:
      f.write('-*' * 80 + '\n')
      f.write(post)




