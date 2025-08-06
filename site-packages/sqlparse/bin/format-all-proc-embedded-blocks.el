;;; format-all-proc-sql-blocks.el --- Format all embedded SQL blocks in Pro*C files -*- lexical-binding: t -*-

;;; Commentary:
;;
;; This function formats **all** embedded SQL blocks in a Pro*C `.pc` source file.
;; It wraps and repeatedly calls `format-next-proc-sql-block`, which handles:
;;
;;   - EXEC SQL ... ;
;;   - EXEC SQL ... END-EXEC;
;;
;; The SQL content inside each block is:
;;   - Extracted (excluding EXEC SQL and terminator)
;;   - Sent to the external SQL formatter `sqlformat`
;;   - Reinserted into the buffer with the formatted version
;;
;; 📦 Requirements:
;; - Install the Python `sqlparse` package:
;;     pip install sqlparse
;; - Ensure `sqlformat` is on your PATH
;;
;; 🧪 Usage:
;; 1. Open a `.pc` Pro*C file.
;; 2. Run: M-x format-all-proc-sql-blocks
;;    → All embedded SQL blocks will be formatted.
;;
;; 🔁 What It Does:
;; - Moves from the top of the buffer.
;; - Formats each EXEC SQL block in turn.
;; - Stops when no further blocks are found.
;;
;; 🎯 Optional Keybinding:
;; (add-hook 'c-mode-hook
;;   (lambda ()
;;     (local-set-key (kbd "C-c C-a") #'format-all-proc-sql-blocks)))
;;
;; 💡 Notes:
;; - Relies on `format-next-proc-sql-block` for actual formatting.
;; - Safe to re-run; formatting is idempotent.
;; - Does not modify EXEC SQL wrappers—only the SQL inside.
;;
;;; Code:

(defun format-all-proc-sql-blocks ()
  "Format all embedded EXEC SQL blocks in the current buffer using sqlformat.
This function repeatedly calls `format-next-proc-sql-block` until no more
SQL blocks are found. It supports both 'EXEC SQL ... ;' and
'EXEC SQL ... END-EXEC;' formats."
  (interactive)
  (save-excursion
    (goto-char (point-min))
    (let ((count 0)
          (keep-going t)
          (last-point -1))
      (while keep-going
        (setq keep-going
              (condition-case err
                  (progn
                    (let ((initial-point (point)))
                      (format-next-proc-sql-block)
                      ;; If point did not advance, assume no more blocks
                      (if (= (point) initial-point)
                          nil
                        (cl-incf count)
                        t)))
                (error
                 (message "Error during formatting: %s" err)
                 nil))))
      (message "Formatted %d embedded SQL block(s)." count))))
