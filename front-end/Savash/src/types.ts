import { ReactElement } from "react";

export const apiUrl = "https://api.codewasabi.xyz";


export interface Class {
    code: number;
    name: string;
    created_at: Date;
}

export function LOGOUT() {
  localStorage.removeItem("role");
  localStorage.removeItem("username");
  document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}

export function getToken(cookie : string) {
  let property = cookie
    .split("; ")
    .find((props: string) => props.startsWith("token="));
  
    if(property){
      return property.substring(6);
    }
    else{
      return "";
    }
}

export interface Tab {
  title : string,
  element : ReactElement
}

export async function getAllClasses(){
  let ans: Class[] = [];
  await fetch(apiUrl + "/classes", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: "bearer " + getToken(document.cookie),
    },
  })
    .then((res) => res.json())
    .then((data) => {
      if (!data || data.length == 0 || !Array.isArray(data)) {
        return;
      }
      console.log(data);
      let dateParsed = data.map((classItem: Class) => {
        return {
          ...classItem,
          created_at: new Date(classItem.created_at),
        };
      });
      ans = dateParsed;
    })
    .catch((err) => {
      alert(err);
      LOGOUT();
      console.error(err);
    });
  return ans;
}

export interface Person {
  name: String;
  username: string;
  email: string;
  role: string;
}

export async function getPeopleFromClass(classID: Number){
  let data = await fetch(apiUrl + "/classes/" + classID + "/people/", {
    method: "GET",
    headers: {
      Authorization: "bearer " + getToken(document.cookie)
    }
  });
  

  let dataParsed = data.json();

  return dataParsed;
}

export async function getAssignment(classID: Number){
  //let data = await fetch(apiUrl + "/cla")
  return classID;
}

export interface Assignment{
  assignment_id? : Number;
  title? : string;
  description? : string;
  questions? : string[];
  choices? : string[][];
  correct_answer? : string[];
  points : Number;
  due_date? : Date;
  created_at? : Date;
}

export function findAssignmentType(data: Assignment){
  if(data.correct_answer){
    return "mcq";
  }
  else if(data.choices){
    return "tfq"
  }
  else if(data.questions){
    return "frq"
  }
  else{
    return "written"
  }
}

export function loadTheme(){
  let themeColorString = localStorage.getItem("theme");
  if(themeColorString){
    let themeColors = JSON.parse(themeColorString);
      let str = "";
      for (const key in themeColors) {
        if (Object.prototype.hasOwnProperty.call(themeColors, key)) {
          str += `--${key}: ${themeColors[key as keyof typeof themeColors]};`;
        }
      }
      console.log(str);
      document.body.setAttribute("style", str);
  }
}

export interface post {
  post_id: number;
  title: string;
  content: string;
  username: string;
  posted_at: Date;
}