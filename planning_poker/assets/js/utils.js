/**
 * Create and append child elements of the given type and given css class to the container element.
 *
 * @param {Array} children An array containing data about the children. each element looks like [tagName, cssClass].
 */
function appendChildrenWithClass(container, children) {
  children.forEach(child_data => {
    let child = document.createElement(child_data[0]);
    child.classList.add(child_data[1]);
    container.appendChild(child);
  });
}

/**
 * Create and append an element to the container which contains the information about the
 * object's JSON-string. This is used to imitate Django's json_script filter.
 *
 * @param {Object} object The object which should be stringified.
 * @param {String} id The id of the element in the DOM.
 * @param {Node} container The container in which the element should be included. Defaults to document.body.
 */
function createJSONElement(object, id, container = document.body) {
  let element = document.createElement('span');
  element.textContent = JSON.stringify(object);
  element.id = id;
  container.appendChild(element);
}

export {appendChildrenWithClass, createJSONElement};
