const loader = document.querySelector('.loader');
const inner = document.querySelector('.inner');
const outer = document.querySelector('.outer');
const percentLabel = document.querySelector('.percent-label');

let loaded = 0;
const total = 100;

function loadData() {
  setTimeout(() => {
    loaded += Math.floor(Math.random() * 10) + 1;
    if (loaded <= total) {
      const angle = (loaded / total) * 360;
      inner.style.clip = `rect(0, 100px, 200px, 0)`;
      outer.style.clip = `rect(0, 100px, 200px, ${100 - angle / 2}px)`;
      percentLabel.textContent = `${loaded}%`;
      loadData();
    } else {
      inner.style.clip = `rect(0, 100px, 200px, 0)`;
      outer.style.clip = `rect(0, 100px, 200px, 0)`;
      percentLabel.textContent = '100%';
      setTimeout(() => {
        loader.style.display = 'none';
      }, 500);
    }
  }, 500);
}

loadData();