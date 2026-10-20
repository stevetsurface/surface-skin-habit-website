// Surface Skin Habit — photo scoring adapter (NOT ACTIVE).
//
// The assessment page only shows the photo step when catalog.json › assessment.scan.enabled is true.
// Until a vendor is licensed this file is a contract, not an implementation.
//
// Vendor class to license (per SSH_Digital_Product_Strategy.md §5): cosmetic-grade scoring that
// outputs aesthetic scores only — Perfect Corp (YouCam Skin Analysis API), Haut.AI, Revieve, Orbo.
// Not Skinive or any vendor that names conditions: naming a disease makes this software a
// registrable medical device under Permenkes 62/2017.
//
// Three questions to ask every vendor before signing:
//   1. On-device or cloud inference? Cloud = facial images leave Indonesia = UU PDP cross-border transfer.
//   2. Do the terms permit deployment in a clinic context?
//   3. Show validation data on Fitzpatrick IV–V faces.
//
// Contract the assessment page expects:
//
//   window.SurfaceScan = {
//     // Resolve with four 0–100 cosmetic scores. Never redness, never a disease name.
//     analyze: async function (file /* File from <input type=file> */) {
//       return { pigmentasi: 0, kerataan: 0, flek: 0, tekstur: 0 };
//     }
//   };
//
// Scores are shown with the fixed wording "pembacaan kosmetik, bukan diagnosis" and are appended
// to the WhatsApp handoff as "Skor scan: pigmentasi 41, kerataan 55, flek 38, tekstur 62".
// The clinic scan under controlled light remains the baseline of record; this is a separate series.
