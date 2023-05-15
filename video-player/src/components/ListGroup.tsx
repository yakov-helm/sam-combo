import { MouseEvent } from "react";
import { useState } from "react";

// Props are inputs to the component, and should be considered immutable
interface Props {
  items: string[];
  heading: string;
  onSelectItem: (item: string) => void;
}

function ListGroup({items, heading, onSelectItem}: Props) {

  // State is like a local variable inside a function; states are mutable
  const [selectedItem, setSelectedItem] = useState("");

  const handleClick = (event: MouseEvent) => {
    let item = event.currentTarget.innerHTML;
    setSelectedItem(item);
    onSelectItem(item);
  }

  return (
    <>
      <h1>{heading}</h1>
      <ul className="list-group">
        {items.map((item) => (
          <li className={selectedItem == item ? "list-group-item active" : "list-group-item"}
            key={item} onClick={handleClick}>
            {item}
          </li>
        ))}
      </ul>
    </>
  );
}

export default ListGroup;

// Both states and props trigger re-rendering and DOM updating

// children -- every component has it, can pass in more complicated things

// React dev tools -- Chrome extension -- reactive tools

// rafce

