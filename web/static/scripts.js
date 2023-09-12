function extractLink(str) {
    const regex = /(https?:\/\/[^\s<]+)/g;
    const match = str.match(regex);
    return match ? match[0] : null;
  }

function addLinkClickListener() {
    const eventDivs = document.querySelectorAll('.box');
  
    eventDivs.forEach((div) => {
      const link = extractLink(div.innerHTML);
  
      if (link) {
        div.style.cursor = 'pointer';
        div.addEventListener('click', () => {
          window.open(link, '_blank');
        });
      }
    });
  }
  
// Call the function after the page has loaded
document.addEventListener('DOMContentLoaded', addLinkClickListener);