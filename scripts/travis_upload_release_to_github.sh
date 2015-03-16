#!/bin/bash


current_tag=$(git describe 2>/dev/null)
remote_url=$(git config --get remote.origin.url)
#remote_url=https://github.com/TwidereProject/Twidere-Android.git

if [[ $remote_url == git@github.com* ]]
then
  user_repo=${remote_url#*:}
elif [[ $remote_url == https://github.com/* ]]
then
  user_repo=${remote_url#*//} # Trim https://
  user_repo=${user_repo#*/} # Trim github.com/
else
  echo "Seems not a github repo, abort"
  exit
fi

user_repo=${user_repo%%.git}

echo $user_repo

if [ -z $current_tag ]
then
  echo "This commit doesn't have tag, proceed without automatic upload"
  exit
elif [ -z $GITHUB_ACCESS_TOKEN ]
then
  echo "No access token given, proceed without automatic upload"
  exit
fi

header_accept="Accept: application/vnd.github.v3+json"
header_type_json="Content-Type: application/json"
header_authorization="Authorization: token "$GITHUB_ACCESS_TOKEN

echo "Has tag "$current_tag", creating release"

echo "{}" | jshon -s "$current_tag" -i "$tag_name" | curl -X POST \
  "https://api.github.com/repos/$user_repo/releases" \
  -H "$header_accept" -H "$header_authorization" -H "$header_type_json" -d -

#find . -iname '*-release.apk' | while read apk
#do
#    echo $apk
#done