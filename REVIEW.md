# REVIEW

1. [PASS] Acceptance 1 (`py quiz.py` / `python quiz.py`): Entry point is correctly wired and interpreter-agnostic. `quiz.py:1-5` calls `app.quiz.main()`, so both launch commands are valid.
2. [PASS] Acceptance 2 (register + login): Registration, login, and password verification flows are implemented with input validation and control flow back to menu. See `app/auth.py:7-91`, `app/data_manage.py:65-113`.
3. [PASS] Acceptance 3 (username/password not human-readable): User credentials are stored as salted PBKDF2 hashes (`username_hash`, `password_hash`) instead of plaintext. See `app/data_manage.py:97-107`, `app/data_manage.py:318-324`.
4. [PASS] Acceptance 4 (missing `question.json` / DAT files should not crash): Missing/broken question file is handled with explicit messages and graceful return; missing/broken DAT files are detected and reset with message. See `app/quiz.py:10-17`, `app/data_manage.py:232-255`.
5. [PASS] Acceptance 5 (normal exit after quiz or error): Program supports controlled exit from finish flow and global `exit` at prompts via exception handling. See `app/quiz.py:29-39`, `app/exit_signal.py:1-9`.
6. [PASS] Acceptance 6 (correctness + score behavior): Per-question correctness is shown; scoring rules match spec (`easy wrong = -1`, `hard correct = +2`). Session score and rates are shown at ending page. See `app/quiz_logic.py:180-186`, `app/quiz_logic.py:243-246`, `app/quiz_logic.py:270-275`, `app/quiz_logic.py:281-293`.
7. [PASS] Acceptance 7 (grade/preference recorded and affects later questions): Results and feedback are persisted, and weighted sampling uses stored per-user weights for next generated batch. See `app/quiz_logic.py:20-23`, `app/quiz_logic.py:42-47`, `app/quiz_logic.py:117-119`, `app/data_manage.py:158-185`, `app/data_manage.py:186-227`.
8. [FAIL] Acceptance 8 (professional question correctness): At least one question/answer pair is incorrect. `data/question.json:53-56` says "`s()` means smooth" but answer is `"False"`; this should be true in `mgcv/gam` context.
9. [PASS] Question list adaptation based on correctness + like/dislike (explicit check): Weight increases on wrong answers, decreases toward baseline on correct answers after prior increases, decreases on dislike, and only increases on like when below baseline; new batches are generated every up-to-10 questions. See `app/data_manage.py:158-185`, `app/quiz_logic.py:20-31`.
10. [FAIL] Security concern: Account recovery can reset the wrong account. Recovery matches only `birthday + last_name`; if multiple users share those values, code resets the first matched account without additional identity proof. See `app/data_manage.py:123-136`.
11. [WARN] Security concern: DAT "encryption" is reversible obfuscation with a static key embedded in source, so data confidentiality is weak if code is available. See `app/data_manage.py:22`, `app/data_manage.py:299-311`.
12. [WARN] Logic/UX issue: Duplicate questions can appear when candidate pool is smaller than requested count because weighted pick switches to with-replacement sampling. See `app/quiz_logic.py:131-134`.
13. [WARN] Missing error handling: DAT writes are not wrapped for `OSError` during normal runtime updates, so disk/permission failures can still crash the app outside startup recovery. See `app/data_manage.py:294-298`, and call sites such as `app/data_manage.py:206-227`.
14. [WARN] Security hardening gap: No login rate limiting or lockout; unlimited credential attempts allow brute-force attempts on local account database. See `app/auth.py:30-43`.
15. [WARN] Code quality: Illegal-input retry logic is duplicated across multiple functions, increasing maintenance overhead and risk of inconsistent behavior. See `app/auth.py:46-86`, `app/quiz_logic.py:62-93`, `app/quiz_logic.py:171-186`, `app/quiz_logic.py:255-267`.
16. [WARN] Robustness gap in auxiliary module: `data/question.py` reads and parses `question.json` without exception handling; direct execution can crash on missing/broken file. See `data/question.py:9-11`.

## Second Detection 

1. [PASS] The fix for question-count input works: current code shows question-bank size and rejects `<= 0` or values larger than total bank size. See `app/quiz_logic.py:62-74`.
2. [PASS] Memory error handling is now added at program entry and main loop level; out-of-memory is reported and the app exits. See `app/quiz.py:10-21`, `app/quiz.py:42-45`.
3. [PASS] Shared illegal-input handling module is added and integrated into quiz/auth flows, reducing duplicated print logic. See `app/illegal_iput.py:1-29`, `app/auth.py:5`, `app/quiz_logic.py:7`.
4. [PASS] The robustness issue in `data/question.py` is fixed by adding file existence and parse/read exception handling. See `data/question.py:10-30`.
5. [WARN] Duplicate-question risk still exists in filtered mode: count validation uses total bank size, but after category/difficulty filtering the pool can be smaller, triggering with-replacement picks and repeated questions. See `app/quiz_logic.py:62-69`, `app/quiz_logic.py:124`, `app/quiz_logic.py:139-142`.
6. [FAIL] Account recovery can still reset the wrong account when multiple users share the same birthday + last name; first match is reset without stronger identity verification. See `app/data_manage.py:126-148`.
7. [FAIL] Professional question correctness issue still exists: in `data/question.json`, the statement "`s()` means smooth" has answer `"False"` but should be true in this context. See `data/question.json:53-56`.
8. [WARN] New storage files are plain JSON text (`*.hash`) and remain human-readable as file content; this conflicts with the non-human-readable storage expectation for score/preference data in the spec features. See `app/data_manage.py:337-339`, `data/scores.hash:1`, `data/feedback.hash:1`.
9. [WARN] Login flow still has no attempt throttling or lockout, so brute-force attempts remain possible on local credentials. See `app/auth.py:9-28`, `app/auth.py:31-41`.
