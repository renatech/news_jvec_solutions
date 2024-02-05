const main=()=>{
  fetch('https://hacker-news.firebaseio.com/v0/topstories.json')
  .then(response => response.json())
  .then(storyIds => {
    // Fetch details for each story
    storyIds.forEach(storyId => {
      fetch(`https://hacker-news.firebaseio.com/v0/item/${storyId}.json`)
        .then(response => response.json())
        .then(story => {
          console.log(story.title);
        });
    });
  });
}

main()