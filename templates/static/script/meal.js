const moreBtn = document.querySelector('.dropdown-btn');
const dropdownMenu = document.querySelector('.dropdown-menu');

moreBtn.addEventListener('click', () => {
dropdownMenu.classList.toggle('show');
});
const titles = document.querySelectorAll('.slideshow-title');
const contents = document.querySelectorAll('.slideshow-content');

titles.forEach(title => {
  title.addEventListener('click', () => {
    const activeTitle = document.querySelector('.slideshow-title.active');
    const activeContent = document.querySelector('.slideshow-content.active');
    activeTitle.classList.remove('active');
    activeContent.classList.remove('active');
    title.classList.add('active');
    const tab = title.getAttribute('data-tab');
    const content = document.querySelector(`.slideshow-content[data-tab="${tab}"]`);
    content.classList.add('active');
  });
});