export let keys = {};

document.addEventListener("keydown", (event) => {
  keys[event.key.toLowerCase()] = true;
});
document.addEventListener("keyup", (event) => {
  keys[event.key.toLowerCase()] = false;
});
