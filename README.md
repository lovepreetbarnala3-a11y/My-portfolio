# My Portfolio

This repository contains a simple personal portfolio website built with HTML. The site is a static single-page layout located at `web_page/Index.html`.

## Preview
Open `web_page/Index.html` in your web browser to view the site. You can run a local static server (for example `Live Server` in VS Code or `python -m http.server`) from the repository root and navigate to `http://localhost:8000/web_page/Index.html`.

## Features
- Simple, responsive HTML structure
- Header, About section, and contact links (email, Instagram, LinkedIn)
- A local profile image (note: the current image path points to a local `D:` drive)

## Project structure

- web_page/Index.html — main web page
- (Add your images, stylesheets and scripts in the repository as needed)

## How to view locally
1. Clone the repository:

   git clone https://github.com/lovepreetbarnala3-a11y/projects.git
2. Change into the repository directory and open the page in your browser:

   - Double-click `web_page/Index.html`, or
   - Start a simple HTTP server from the repository root:

     python -m http.server 8000

   Then open: `http://localhost:8000/web_page/Index.html`

- HTML improvements: Consider these small fixes to improve accessibility and correctness:
  - Use consistent lowercase tag names for HTML and CSS (e.g., `<style>` instead of `<Style>`).
  - Add `alt` text for images (already present, but make it descriptive).
  - Remove stray or broken tags (there is a stray `</a>` and a malformed `<[...]` in the file). Validate with the W3C HTML validator.
  - Move inline styles to a separate stylesheet (e.g., `web_page/style.css`).

## Accessibility tips
- Ensure semantic headings are used in order (h1 → h2 → h3).
- Provide sufficient color contrast for text and interactive elements.
- Add keyboard focus styles and ensure links are keyboard-navigable.

## Contributing
If you want to improve this repo:
1. Fork the repository
2. Create a branch for your changes
3. Make your edits (e.g., fix image path, add CSS, add assets)
4. Open a pull request with a description of your changes

## License
Add a license file if you want to make the project open-source. For example, create a `LICENSE` with the MIT license.

## Contact
Lovepreet Barnala — lovepreetbarnala3@gmail.com
LinkedIn: https://www.linkedin.com/in/lovepreet-barnala-45b0a924b/
Instagram: https://www.instagram.com/love._o5
