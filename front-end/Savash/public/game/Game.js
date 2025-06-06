console.log("Game JS Loaded");

import * as THREE from "three";

import { apiUrl } from "../../src/types.js";

import { CameraManager } from "./camera.js";

import { PlayerController } from "./Player.js";

import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { keys } from "./input.js";

const hostBtn = document.getElementById("host");
const joinBtn = document.getElementById("join");

export function createScene() {
  const gameWindow = document.getElementById("render-target");
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x112277);

  const lightLayer = 10;

  const camera = new CameraManager();
  camera.camera.layers.enable(lightLayer); // Enable layer 10 for the camera

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(gameWindow.clientWidth, gameWindow.clientHeight);
  renderer.shadowMap.enabled = true; // Enable shadow mapping
  renderer.shadowMap.type = THREE.PCFSoftShadowMap; // Use soft shadows
  gameWindow.appendChild(renderer.domElement);


  const dirLight = new THREE.DirectionalLight(0xffeebb, 5);
  dirLight.rotation.set(-Math.PI / 2, -Math.PI/5, 0); // Set the light direction
  dirLight.castShadow = true; // Enable shadow casting for the light
  dirLight.shadow.mapSize.width = 1024 * 2; // Set shadow map size
  dirLight.shadow.mapSize.height = 1024 * 2; // Set shadow map size
  dirLight.shadow.camera.near = 0.5; // Near plane for shadow camera
  dirLight.shadow.camera.far = 100; // Far plane for shadow camera
  dirLight.shadow.camera.left = -80; // Left plane for shadow camera
  dirLight.shadow.camera.right = 80; // Right plane for shadow camera
  dirLight.shadow.camera.top = 50; // Top plane for shadow camera
  dirLight.shadow.camera.bottom = -50; // Bottom plane for shadow camera
  dirLight.layers.set(lightLayer); // Enable layer 0 for the light
  dirLight.layers.disable(0);
  scene.add(dirLight);

  const ambientLight = new THREE.AmbientLight(0x0000f0, 1); // Soft white light
  scene.add(ambientLight);

  const lightHelper = new THREE.DirectionalLightHelper(dirLight, 5);
  scene.add(lightHelper);


  //load gltf model
  const gltfLoader = new GLTFLoader();

  const playerController = new PlayerController();

  let marker = new THREE.Mesh(
    new THREE.SphereGeometry(0.1, 16, 16),
    new THREE.MeshBasicMaterial({ color: 0xffff00 })
  );

  scene.add(marker);

  let omarker = new THREE.Mesh(
    new THREE.SphereGeometry(0.1, 16, 16),
    new THREE.MeshBasicMaterial({
      color: 0xffff00,
    })
  );

  scene.add(omarker);

  gltfLoader.load("/game/models/trackbig/trackbig.glb", (gltf) => {
    let track = gltf.scene;
    track.scale.set(200, 200, 200); // Scale the model down

    // Enable shadow casting for all meshes in the loaded GLTF model
    track.traverse((child) => {
      if (child.isMesh) {
        child.receiveShadow = false; // Only cast shadow, don't receive
        child.castShadow = false; // Enable shadow casting
        child.layers.set(0); // Enable layer 0 for the track model
      }
    });

    scene.add(track);
  });

  gltfLoader.load("/game/models/car/car.glb", (gltf) => {
    playerController.player = gltf.scene;
    playerController.player.scale.set(0.5, 0.5, 0.5); // Scale the model down
    playerController.player.layers.set(lightLayer); // Enable layer 0 for the player model

    // Enable shadow casting for all meshes in the loaded GLTF model
    playerController.player.traverse((child) => {
      if (child.isMesh) {
        child.castShadow = true;
        child.receiveShadow = false; // Only cast shadow, don't receive
      }
    });

    scene.add(playerController.player);

    waitForStart();
  });

  async function waitForStart() {
    tick();
    document.getElementById("loading").style.display = "none";
    hostBtn.addEventListener("click", async () => {
      document.getElementById("start").style.display = "none";

      let name = prompt("Enter your name:");

      console.log(
        JSON.stringify({
          host_name: name,
          min: 0
        })
      );

      let gameCode = await fetch(apiUrl + "/games/", {
        method: "POST",
        body: JSON.stringify({
          host_name: name,
          min: 0
        }),
      });

      gameCode = await gameCode.text();

      console.log("Game Code:", gameCode);

      gameCode = Number(gameCode);
      activateTicking();
    });
  }

  function activateTicking() {
    let ticking = setInterval(() => {
      tick();
    }, 16);
  }

  function tick() {
    playerController.tick(0.016); // Assuming 60 FPS, so deltaTime is ~0.016 seconds

      camera.cameraOrigin.copy(playerController.position);
      camera.updateCameraPosition();
     

      let translationalSpeed = new THREE.Vector2(
        playerController.velocity.x,
        playerController.velocity.z
      ).length();

      camera.camera.fov = Math.min(180, translationalSpeed / 10 + camera.fov); // Adjust FOV based on speed
      camera.cameraAzimuth = playerController.rotation.y*180 / Math.PI + 90; // Update camera azimuth based on player rotation
      camera.updateCameraPosition();

      playerController.accelerationRot.y = 0;

      if (keys["a"]) {
        if (keys["s"]) {
          playerController.accelerationRot.y = -translationalSpeed; // Rotate right
        } else {
          playerController.accelerationRot.y = translationalSpeed; // Rotate right
        }
      }
      if (keys["d"]) {
        if (keys["s"]) {
          playerController.accelerationRot.y = translationalSpeed; // Rotate right
        } else {
          playerController.accelerationRot.y = -translationalSpeed; // Rotate right
        }
      }

      dirLight.position.copy(playerController.position);
      dirLight.position.y += 2; // Keep the light above the player
  }

  function draw() {
    renderer.render(scene, camera.camera);
  }

  function start() {
    renderer.setAnimationLoop(draw);
  }

  function stop() {
    renderer.setAnimationLoop(null);
  }

  return {
    start,
    stop,
  };
}

function getGroundHeight(groundTexture, u, v) {
  if (!groundTexture.image) return null;

  // Create a canvas and draw the image if not already done
  if (!groundTexture._canvas) {
    const canvas = document.createElement("canvas");
    canvas.width = groundTexture.image.width;
    canvas.height = groundTexture.image.height;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(groundTexture.image, 0, 0);
    groundTexture._canvas = canvas;
    groundTexture._ctx = ctx;
  }

  const x = Math.floor(u * groundTexture.image.width);
  const y = Math.floor(v * groundTexture.image.height);

  const pixel = groundTexture._ctx.getImageData(x, y, 1, 1).data;
  // pixel is [r, g, b, a]
  return { r: pixel[0], g: pixel[1], b: pixel[2], a: pixel[3] };
}
