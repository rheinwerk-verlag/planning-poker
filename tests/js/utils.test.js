import {appendChildrenWithClass, createJsonElement} from "../../planning_poker/assets/js/utils.js";

test('appendChildrenWithClass', () => {
  let container = document.createElement('body');
  let children = [['div', 'nav'], ['span', 'comment'], ['video', 'autoplay']];
  appendChildrenWithClass(container, children);
  for (let i = 0; i < children.length; i++){
    expect(container.children[i].tagName.toLowerCase()).toBe(children[i][0]);
    expect(container.children[i].className).toBe(children[i][1]);
  }
});

test('createJsonElement', () => {
  let object = {'foo': null, 'bar': ['b', 'a', 'z']};
  let id = 'foo-bar-baz';
  let container = document.createElement('body');
  createJsonElement(object, id, container);
  let jsonElement = container.querySelector(`#${id}`);
  expect(JSON.parse(jsonElement.innerHTML)).toEqual(object);
});
