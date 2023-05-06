import { API_LIST_ALL } from "../../enviroments";


const getPhotos = (): any[] => {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", API_LIST_ALL, false);
  xhr.send();
  const json = JSON.parse(xhr.response);
  // console.log("GOT LIST OF FILES");
  // console.log(json);
  // console.log("DONE LIST OF FILES");
  return json["files"];
}

const photos = getPhotos();

export default photos;
