import * as THREE from "three";

import { keys } from "./input.js";

export class PlayerController {
  constructor() {

    this.position = new THREE.Vector3(25, 0, 10);
    this.rotation = new THREE.Euler(0, -Math.PI/2, 0);
    this.velocity = new THREE.Vector3(0, 0, 0);
    this.acceleration = new THREE.Vector3(0, 0, 0);
    this.speed = 100;
    this.maxSpeed = 100.0;
    this.player = null;
  }
  tick(deltaTime) {
    
    this.acceleration.set(0, 0, 0);

    // Update position based on velocity
    let x = 0;

    let y = 0;

    if (keys["w"]) {
      x = -this.speed; // Move forward
    } else if (keys["s"]) {
      x = this.speed/2; // Move backward
    }

    this.acceleration.set(x, 0, y);
    this.acceleration.applyEuler(this.rotation, "XYZ"); // Apply rotation to acceleration

    this.position.addScaledVector(this.velocity, deltaTime);

    // Apply acceleration
    this.velocity.addScaledVector(this.acceleration, deltaTime);

    this.velocity.clampLength(0, this.maxSpeed); // Limit speed]
    this.velocity.multiplyScalar(0.9); // Dampen velocity

    // Update player mesh position and rotation
    this.player.position.copy(this.position);
    this.player.rotation.copy(this.rotation);
  }
}