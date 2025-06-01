console.log("Setup JS Loaded");
import { createScene } from "./Game.js";

window.addEventListener("load", () => {
  const gameWindow = document.getElementById("render-target");
  if (!gameWindow) {
    console.error("Render target not found");
    return;
  }
    window.ui = {
        gameWindow: gameWindow,
    };
  window.scene = createScene();
  window.scene.start();
});
