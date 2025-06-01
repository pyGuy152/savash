console.log("Game JS Loaded");

import * as THREE from "three";

import { CameraManager } from "./camera.js";

import { PlayerController } from "./Player.js";

import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { keys } from "./input.js";

export function createScene() {
  const gameWindow = document.getElementById("render-target");
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x777777);

  const camera = new CameraManager();

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(gameWindow.clientWidth, gameWindow.clientHeight);
  renderer.shadowMap.enabled = true; // Enable shadow mapping
  renderer.shadowMap.type = THREE.PCFSoftShadowMap; // Use soft shadows
  gameWindow.appendChild(renderer.domElement);

  const dirLight = new THREE.DirectionalLight(0xffffee, 2);
  dirLight.position.set(3, 5, 2);
  dirLight.castShadow = true; // Enable shadow casting for the light
  dirLight.shadow.mapSize.width = 1024 * 2; // Set shadow map size
  dirLight.shadow.mapSize.height = 1024 * 2; // Set shadow map size
  dirLight.shadow.camera.near = 0.5; // Near plane for shadow camera
  dirLight.shadow.camera.far = 100; // Far plane for shadow camera
  dirLight.shadow.camera.left = -10; // Left plane for shadow camera
  dirLight.shadow.camera.right = 10; // Right plane for shadow camera
  dirLight.shadow.camera.top = 10; // Top plane for shadow camera
  dirLight.shadow.camera.bottom = -10; // Bottom plane for shadow camera
  scene.add(dirLight);

  const ambientLight = new THREE.AmbientLight(0x4040f0, 0.8); // Soft white light
  scene.add(ambientLight);

  const lightHelper = new THREE.DirectionalLightHelper(dirLight, 0.5);
  scene.add(lightHelper);

  const texLoader = new THREE.TextureLoader();

  const groundTexture = texLoader.load("/game/models/track/track.png");

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
      color: 0xffff00
    })
  );

  scene.add(omarker);

  gltfLoader.load("/game/models/track/track.glb", (gltf) => {
    let track = gltf.scene;
    track.scale.set(4, 2, 4); // Scale the model down

    // Enable shadow casting for all meshes in the loaded GLTF model
    track.traverse((child) => {
      if (child.isMesh) {
        child.receiveShadow = true; // Only cast shadow, don't receive
      }
    });

    scene.add(track);
  });

  gltfLoader.load("/game/models/car/car.glb", (gltf) => {
    playerController.player = gltf.scene;
    playerController.player.scale.set(0.01, 0.01, 0.01); // Scale the model down

    // Enable shadow casting for all meshes in the loaded GLTF model
    playerController.player.traverse((child) => {
      if (child.isMesh) {
        child.castShadow = true;
        child.receiveShadow = false; // Only cast shadow, don't receive
      }
    });

    scene.add(playerController.player);

    activateTicking();
  });

  function activateTicking() {
    let ticking = setInterval(() => {
      playerController.tick(0.016); // Assuming 60 FPS, so deltaTime is ~0.016 seconds
      camera.cameraOrigin.copy(playerController.position);
      camera.updateCameraPosition();

      playerController.position.y += 0.5;

      let origin =
        1.1 -
        getGroundHeight(
          groundTexture,
          (playerController.position.x / 29) * 0.5 + 0.5,
          (playerController.position.z / 29) * 0.25 + 0.5
        ).r /
          100.0;

      let forwardVector = new THREE.Vector3(
        -Math.cos(playerController.rotation.y),
        0,
        Math.sin(playerController.rotation.y)
      ).add(playerController.position);

      
      marker.position.copy(forwardVector);
      omarker.position.copy(playerController.position);

      let forward =
        1.1 -
        getGroundHeight(
          groundTexture,
          (forwardVector.x / 29) * 0.5 + 0.5,
          (forwardVector.z / 29) * 0.25 + 0.5
        ).r /
          100.0;

      playerController.position.y = origin;
      playerController.rotation.z = Math.min(
        (origin - forward),
        Math.PI / 3
      );

      let translationalSpeed = new THREE.Vector2(
        playerController.velocity.x,
        playerController.velocity.z
      ).length();
      camera.camera.fov = translationalSpeed + 80; // Adjust FOV based on speed
      if (keys["a"]) {
        if (keys["s"]) {
          playerController.rotation.y -= 0.003 * translationalSpeed; // Rotate right
        } else {
          playerController.rotation.y += 0.003 * translationalSpeed; // Rotate right
        }
      }
      if (keys["d"]) {
        if (keys["s"]) {
          playerController.rotation.y += 0.003 * translationalSpeed; // Rotate right
        } else {
          playerController.rotation.y -= 0.003 * translationalSpeed; // Rotate right
        }
      }
      dirLight.position.copy(playerController.position);
      dirLight.position.add(new THREE.Vector3(3, 5, 2));
      dirLight.target.position.copy(playerController.position);
      scene.add(dirLight.target);
    }, 16);
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
