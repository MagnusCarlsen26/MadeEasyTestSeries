# Answer Decoding Logic

## Encrypted Field
The `CORRECT_ANSWER` field in the API response is encrypted/hashed. However, the hashes are static for standard Multiple Choice Questions (MCQ).

## MCQ Mapping (Types 7 & 1)
| Encrypted String | Result |
| :--- | :--- |
| `Dsdj/LJX8pBs6q+b96fwiQ==` | **Option 1** |
| `fhPK/WKkcuYMengj9uY6cg==` | **Option 2** |
| `9m/iwvJKC6coEJr5HJJczQ==` | **Option 3** |
| `Wkw/v0ACIC+JhZVbmq0HcA==` | **Option 4** |

## NAT Questions (Type 2)
For Numerical Answer Type (NAT) questions, the readable answer value is mirrored in the `OPT1` field of the question object, even though there are no visual options.

## MSQ Questions (Type 5)
Multiple Select Questions use unique Base64 strings for every combination of correct answers. These require manual mapping or a known key to decrypt.
