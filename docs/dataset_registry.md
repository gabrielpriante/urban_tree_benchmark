# Dataset Registry

> **Status: INITIALIZED, NOT VERIFIED.** No dataset characteristic in this
> registry has been checked against a primary source yet. Every field is
> marked **Requires verification** until it is confirmed and cited.

_Last updated: 2026-11-21_

## How to use this registry

- Fill in a field only after confirming it from a primary source (original
  paper, official repository, data portal, or license file).
- Record the source for each verified field in the entry's **Sources** list,
  with the access date.
- Mark conflicting information as **Conflicting**, list both sources, and
  explain the discrepancy in the notes.
- **Preliminary leads** are unverified pointers to help with the lookup. They
  are **not** registry data and must not be cited.

## Field definitions

| Field | Definition |
|---|---|
| Dataset name | Official name and common abbreviation |
| Source URL | Official landing page, repository, or data portal |
| Publication / version | Citing publication(s) and dataset version or release date |
| Geography | Countries, regions, sites, or cities covered |
| Urban relevance | Share or type of urban imagery: none / partial / primary |
| Image count | Number of images or tiles, by split if available |
| Resolution | Ground sampling distance (cm/pixel) and sensor/platform |
| Annotation format | Geometry (bounding box, polygon, point, mask) and file format |
| Ground-truth methodology | How labels were made (field survey, manual image annotation, LiDAR-derived, etc.) and QA process |
| Training/test separation | Official splits and whether the test data is independent |
| Licensing | Data license and any usage restrictions |
| Model-training overlap | Known use in training the models we plan to evaluate |
| Research suitability | Assessment against `selection_criteria.md` (fill in after verification) |
| Verification status | Not started / In progress / Verified (date) |

## Summary table

| # | Dataset | Type | Urban relevance | Verification status |
|---|---|---|---|---|
| 1 | NEON Tree Evaluation | Source dataset | Requires verification | Not started |
| 2 | OAM-TCD | Source dataset | Requires verification | Not started |
| 3 | Urban Tree Detection (Ventura et al.) | Source dataset | Requires verification | Not started |
| 4 | DeepTrees-Halle | Source dataset | Requires verification | Not started |
| 5 | MillionTrees | **Aggregation / benchmark framework** | Requires verification | Not started |

---

## 1. NEON Tree Evaluation

| Field | Value |
|---|---|
| Dataset name | NEON Tree Evaluation |
| Source URL | Requires verification |
| Publication / version | Requires verification |
| Geography | Requires verification |
| Urban relevance | Requires verification |
| Image count | Requires verification |
| Resolution | Requires verification |
| Annotation format | Requires verification |
| Ground-truth methodology | Requires verification |
| Training/test separation | Requires verification |
| Licensing | Requires verification |
| Model-training overlap | Requires verification. **High priority**: check its relationship to DeepForest's pretrained model and training data. |
| Research suitability | Pending verification |
| Verification status | Not started |

**Preliminary leads (unverified):** Associated with the Weecology lab and the
DeepForest authors (Weinstein et al.). Reportedly derived from National
Ecological Observatory Network (NEON) airborne data at US sites.

**Sources:** _None recorded yet._

---

## 2. OAM-TCD

| Field | Value |
|---|---|
| Dataset name | OAM-TCD |
| Source URL | Requires verification |
| Publication / version | Requires verification |
| Geography | Requires verification |
| Urban relevance | Requires verification |
| Image count | Requires verification |
| Resolution | Requires verification |
| Annotation format | Requires verification |
| Ground-truth methodology | Requires verification |
| Training/test separation | Requires verification |
| Licensing | Requires verification. Check whether imagery and annotations have different licenses. |
| Model-training overlap | Requires verification |
| Research suitability | Pending verification |
| Verification status | Not started |

**Preliminary leads (unverified):** Reportedly a tree cover delineation
dataset built on OpenAerialMap imagery and released by Restor (Veitch-Michaelis
et al.). Check whether annotations include individual trees, canopy groups,
or both, since this affects counting.

**Sources:** _None recorded yet._

---

## 3. Urban Tree Detection (Ventura et al.)

| Field | Value |
|---|---|
| Dataset name | Urban Tree Detection (Ventura et al.). Confirm official name |
| Source URL | Requires verification |
| Publication / version | Requires verification |
| Geography | Requires verification |
| Urban relevance | Requires verification |
| Image count | Requires verification |
| Resolution | Requires verification |
| Annotation format | Requires verification |
| Ground-truth methodology | Requires verification |
| Training/test separation | Requires verification |
| Licensing | Requires verification |
| Model-training overlap | Requires verification |
| Research suitability | Pending verification |
| Verification status | Not started |

**Preliminary leads (unverified):** Reportedly focused on urban trees in
California. Annotation geometry may be point-based rather than boxes. Check
this, since it affects compatibility with box-based detectors.

**Sources:** _None recorded yet._

---

## 4. DeepTrees-Halle

| Field | Value |
|---|---|
| Dataset name | DeepTrees-Halle. Confirm official name |
| Source URL | Requires verification |
| Publication / version | Requires verification |
| Geography | Requires verification |
| Urban relevance | Requires verification |
| Image count | Requires verification |
| Resolution | Requires verification |
| Annotation format | Requires verification |
| Ground-truth methodology | Requires verification |
| Training/test separation | Requires verification |
| Licensing | Requires verification |
| Model-training overlap | Requires verification |
| Research suitability | Pending verification |
| Verification status | Not started |

**Preliminary leads (unverified):** The name suggests coverage of Halle
(Saale), Germany. Confirm the publishing group, data access, and whether it is
a standalone dataset or part of a larger toolkit.

**Sources:** _None recorded yet._

---

## 5. MillionTrees (aggregation / benchmark framework)

> **Not an independent source dataset.** MillionTrees is treated as an
> aggregation or benchmark framework that combines existing datasets. Its
> component datasets must be identified and assessed individually. Ground
> truth, licensing, and training overlap come from each component source, not
> from MillionTrees itself.

| Field | Value |
|---|---|
| Dataset name | MillionTrees |
| Source URL | Requires verification |
| Publication / version | Requires verification. Record the exact release used, because component sets may change between versions |
| Component datasets | Requires verification. List each source dataset and check for overlap with entries 1–4 |
| Geography | Requires verification (aggregate of components) |
| Urban relevance | Requires verification |
| Image count | Requires verification |
| Resolution | Requires verification (likely varies by component) |
| Annotation format | Requires verification (check how box/point/polygon tasks are organized) |
| Ground-truth methodology | Inherited from component datasets. Requires verification per component |
| Training/test separation | Requires verification. Check the framework's split definitions against the original dataset splits |
| Licensing | Requires verification per component. Framework license may differ from component licenses |
| Model-training overlap | Requires verification. **High priority**: check whether evaluated models were trained on any components |
| Research suitability | Pending verification |
| Verification status | Not started |

**Preliminary leads (unverified):** Reportedly developed by the Weecology lab
(same group as DeepForest). This makes the training-overlap check especially
important.

**Sources:** _None recorded yet._

---

## Entry template (for new candidates)

```markdown
## N. <Dataset name>

| Field | Value |
|---|---|
| Dataset name | |
| Source URL | Requires verification |
| Publication / version | Requires verification |
| Geography | Requires verification |
| Urban relevance | Requires verification |
| Image count | Requires verification |
| Resolution | Requires verification |
| Annotation format | Requires verification |
| Ground-truth methodology | Requires verification |
| Training/test separation | Requires verification |
| Licensing | Requires verification |
| Model-training overlap | Requires verification |
| Research suitability | Pending verification |
| Verification status | Not started |

**Preliminary leads (unverified):**

**Sources:**
- <field(s)>: <citation or URL>, accessed YYYY-MM-DD
```
