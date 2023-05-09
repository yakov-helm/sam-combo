import { API_LIST_DIRS, API_LIST_ALL } from "../../enviroments";


let dirname = "";


const getFiles = (endpoint: string): any[] => {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", endpoint, false);
  xhr.send();
  const json = JSON.parse(xhr.response);
  return json["files"];
};


export const getPhotos = (): any[] => {
  // get the photos -- one case or the other
  if (dirname === "") {
    // show the available dirs
    return getFiles(API_LIST_DIRS);
  } else {
  // show the files in the dir
  return getFiles(API_LIST_ALL + '/' + dirname);
  }
};


export const setDir = (newDirName: string): string => {
  // go into the specific directory
  if (dirname === "") {
    dirname = newDirName;
    console.log("Changed default dir name to", dirname);
    return "";
  } else {
    return dirname;
  }
};


export const getDir = (): string => {
  return dirname;
};
