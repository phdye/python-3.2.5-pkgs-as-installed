;;; Usage
;;;
;;; - Select an embedded SQL region inside EXEC SQL ...;.
;;; - Run M-x format-proc-embedded-sql.
;;; 
;;; It will:
;;; 
;;; Send the region to sqlformat.
;;; 
;;; Capture the formatted result.
;;; 
;;; Replace the original region with the formatted SQL.
;;; 
;;; Optional: Bind to a Key
;;; To bind it to a convenient key (e.g. C-c C-f in c-mode):
;
; (add-hook 'c-mode-hook
;           (lambda ()
;             (local-set-key (kbd "C-c C-f") #'format-proc-embedded-sql)))

(defun format-proc-embedded-sql (start end)
  "Format embedded SQL in a selected region using sqlformat."
  (interactive "r")
  (let ((formatted-sql-buffer "*Formatted SQL*"))
    (if (use-region-p)
        (progn
          (shell-command-on-region
           start end
           "sqlformat -r -k upper -s -"  ; change options here if needed
           formatted-sql-buffer
           nil ; do not replace region automatically
           "*SQL Format Errors*" t)
          (with-current-buffer formatted-sql-buffer
            (let ((formatted (buffer-string)))
              (delete-region start end)
              (goto-char start)
              (insert formatted)))
          (kill-buffer formatted-sql-buffer))
      (message "No region selected."))))
