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

export interface Assignment {
  assignment_id : Number;
  title : string,
  description : string,
  due_date : Date,
  created_at : Date
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
      if (!data || data.length == 0) {
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