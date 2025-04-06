const handsontableContainer = document.getElementById('handsontable-container')
let hot;

params = new URLSearchParams(window.location.search);
const fileUrl = params.get("file")
const targetRow = parseInt(params.get("row"), 10); // Will be NaN if not provided

fetch(fileUrl)
  .then(response => {
    if (!response.ok) {
      console.log(fileUrl)
      throw new Error("Failed to fetch the CSV file");
    }
    return response.text();
  })
  .then(csvText => {
    const data = Papa.parse(csvText, {
      header: true,
      skipEmptyLines: true
    });

    handsontableContainer.innerHTML = '';
    handsontableContainer.className = '';
    document.querySelector('.spinner').remove();

    hot = new Handsontable(handsontableContainer, {
      data: data.data,
      rowHeaders: true,
      colHeaders: data.meta.fields,
      columnSorting: true,
      width: '100%',
      licenseKey: 'non-commercial-and-evaluation',
    });

    if (!isNaN(targetRow)) {
      hot.scrollViewportTo(targetRow);
      hot.selectCell(targetRow, 0);
    
      setTimeout(() => {
        const cell = hot.getCell(targetRow, 0);
        if (cell) {
          cell.scrollIntoView({
            behavior: 'smooth',
            block: 'center',
            inline: 'center'
          });
        }
      }, 100); // Short delay ensures Handsontable has rendered the cell
      // Apply a custom class to the row
      for (let col = 0; col < data.meta.fields.length; col++) {
        hot.setCellMeta(targetRow, col, 'className', 'highlighted-cell');
      }
      hot.render(); // important to apply styles
    }
  })
  .catch(error => {
    console.error("Error loading CSV:", error);
  });