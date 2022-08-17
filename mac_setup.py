import subprocess
import base64
import time
import sys
import os


# base64 encoded string of larger script used to apply images as icons to a file on Mac
FILEICON = "IyEvdXNyL2Jpbi9lbnYgYmFzaAoKIyMjCiMgSG9tZSBwYWdlOiBodHRwczovL2dpdGh1Yi5jb20vbWtsZW1lbnQwL2ZpbGVpY29uCiMgQXV0aG9yOiAgIE1pY2hhZWwgS2xlbWVudCA8bWtsZW1lbnQwQGdtYWlsLmNvbT4gKGh0dHA6Ly9zYW1lMnUubmV0KQojIEludm9rZSB3aXRoOgojICAgLS12ZXJzaW9uIGZvciB2ZXJzaW9uIGluZm9ybWF0aW9uCiMgICAtLWhlbHAgZm9yIHVzYWdlIGluZm9ybWF0aW9uCiMjIwoKIyAtLS0gU1RBTkRBUkQgU0NSSVBULUdMT0JBTCBDT05TVEFOVFMKCmtUSElTX05BTUU9JHtCQVNIX1NPVVJDRSMjKi99CmtUSElTX0hPTUVQQUdFPSdodHRwczovL2dpdGh1Yi5jb20vbWtsZW1lbnQwL2ZpbGVpY29uJwprVEhJU19WRVJTSU9OPSd2MC4zLjEnICMgTk9URTogVGhpcyBhc3NpZ25tZW50IGlzIGF1dG9tYXRpY2FsbHkgdXBkYXRlZCBieSBgbWFrZSB2ZXJzaW9uIFZFUj08bmV3VmVyPmAgLSBETyBrZWVwIHRoZSAndicgcHJlZml4LgoKdW5zZXQgQ0RQQVRIICAjIFRvIHByZXZlbnQgdW5wcmVkaWN0YWJsZSBgY2RgIGJlaGF2aW9yLgoKIyAtLS0gQmVnaW46IFNUQU5EQVJEIEhFTFBFUiBGVU5DVElPTlMKCmRpZSgpIHsgZWNobyAiJGtUSElTX05BTUU6IEVSUk9SOiAkezE6LSJBQk9SVElORyBkdWUgdG8gdW5leHBlY3RlZCBlcnJvci4ifSIgMT4mMjsgZXhpdCAkezI6LTF9OyB9CmRpZVN5bnRheCgpIHsgZWNobyAiJGtUSElTX05BTUU6IEFSR1VNRU5UIEVSUk9SOiAkezE6LSJJbnZhbGlkIGFyZ3VtZW50KHMpIHNwZWNpZmllZC4ifSBVc2UgLWggZm9yIGhlbHAuIiAxPiYyOyBleGl0IDI7IH0KCiMgU1lOT1BTSVMKIyAgIG9wZW5VcmwgPHVybD4KIyBERVNDUklQVElPTgojICAgT3BlbnMgdGhlIHNwZWNpZmllZCBVUkwgaW4gdGhlIHN5c3RlbSdzIGRlZmF1bHQgYnJvd3Nlci4Kb3BlblVybCgpIHsKICBsb2NhbCB1cmw9JDEgcGxhdGZvcm09JCh1bmFtZSkgY21kPSgpCiAgY2FzZSAkcGxhdGZvcm0gaW4KICAgICdEYXJ3aW4nKSAjIE9TWAogICAgICBjbWQ9KCBvcGVuICIkdXJsIiApCiAgICAgIDs7CiAgICAnQ1lHV0lOXycqKSAjIEN5Z3dpbiBvbiBXaW5kb3dzOyBtdXN0IGNhbGwgY21kLmV4ZSB3aXRoIGl0cyBgc3RhcnRgIGJ1aWx0aW4KICAgICAgY21kPSggY21kLmV4ZSAvYyBzdGFydCAnJyAiJHVybCAiICkgICMgISEgTm90ZSB0aGUgcmVxdWlyZWQgdHJhaWxpbmcgc3BhY2UuCiAgICAgIDs7CiAgICAnTUlOR1czMl8nKikgIyBNU1lTIG9yIEdpdCBCYXNoIG9uIFdpbmRvd3M7IHRoZXkgY29tZSB3aXRoIGEgVW5peCBgc3RhcnRgIGJpbmFyeQogICAgICBjbWQ9KCBzdGFydCAnJyAiJHVybCIgKQogICAgICA7OwogICAgKikgIyBPdGhlcndpc2UsIGFzc3VtZSBhIEZyZWVkZXNrdG9wLWNvbXBsaWFudCBPUywgd2hpY2ggaW5jbHVkZXMgbWFueSBMaW51eCBkaXN0cm9zLCBQQy1CU0QsIE9wZW5Tb2xhcmlzLCAuLi4KICAgICAgY21kPSggeGRnLW9wZW4gIiR1cmwiICkKICAgICAgOzsKICBlc2FjCiAgIiR7Y21kW0BdfSIgfHwgeyBlY2hvICJDYW5ub3QgbG9jYXRlIG9yIGZhaWxlZCB0byBvcGVuIGRlZmF1bHQgYnJvd3NlcjsgcGxlYXNlIGdvIHRvICckdXJsJyBtYW51YWxseS4iID4mMjsgcmV0dXJuIDE7IH0KfQoKIyBQcmludHMgdGhlIGVtYmVkZGVkIE1hcmtkb3duLWZvcm1hdHRlZCBtYW4tcGFnZSBzb3VyY2UgdG8gc3Rkb3V0LgpwcmludE1hblBhZ2VTb3VyY2UoKSB7CiAgL3Vzci9iaW4vc2VkIC1uIC1lICQnL146IDw8XCdFT0ZfTUFOX1BBR0VcJy8sL15FT0ZfTUFOX1BBR0UvIHsgcy8vLzsgdFxucDt9JyAiJEJBU0hfU09VUkNFIgp9CgojIE9wZW5zIHRoZSBtYW4gcGFnZSwgaWYgaW5zdGFsbGVkOyBvdGhlcndpc2UsIHRyaWVzIHRvIGRpc3BsYXkgdGhlIGVtYmVkZGVkIE1hcmtkb3duLWZvcm1hdHRlZCBtYW4tcGFnZSBzb3VyY2U7IGlmIGFsbCBlbHNlIGZhaWxzOiB0cmllcyB0byBkaXNwbGF5IHRoZSBtYW4gcGFnZSBvbmxpbmUuCm9wZW5NYW5QYWdlKCkgewogIGxvY2FsIHBhZ2VyIGVtYmVkZGVkVGV4dAogIGlmICEgbWFuIDEgIiRrVEhJU19OQU1FIiAyPi9kZXYvbnVsbDsgdGhlbgogICAgIyAybmQgYXR0ZW1wdDogaWYgcHJlc2VudCwgZGlzcGxheSB0aGUgZW1iZWRkZWQgTWFya2Rvd24tZm9ybWF0dGVkIG1hbi1wYWdlIHNvdXJjZQogICAgZW1iZWRkZWRUZXh0PSQocHJpbnRNYW5QYWdlU291cmNlKQogICAgaWYgW1sgLW4gJGVtYmVkZGVkVGV4dCBdXTsgdGhlbgogICAgICBwYWdlcj0nbW9yZScKICAgICAgY29tbWFuZCAtdiBsZXNzICY+L2Rldi9udWxsICYmIHBhZ2VyPSdsZXNzJyAjIHNlZSBpZiB0aGUgbm9uLXN0YW5kYXJkIGBsZXNzYCBpcyBhdmFpbGFibGUsIGJlY2F1c2UgaXQncyBwcmVmZXJhYmxlIHRvIHRoZSBQT1NJWCB1dGlsaXR5IGBtb3JlYAogICAgICBwcmludGYgJyVzXG4nICIkZW1iZWRkZWRUZXh0IiB8ICIkcGFnZXIiCiAgICBlbHNlICMgM3JkIGF0dGVtcHQ6IG9wZW4gdGhlIHRoZSBtYW4gcGFnZSBvbiB0aGUgdXRpbGl0eSdzIHdlYnNpdGUKICAgICAgb3BlblVybCAiJHtrVEhJU19IT01FUEFHRX0vZG9jLyR7a1RISVNfTkFNRX0ubWQiCiAgICBmaQogIGZpCn0KCiMgUHJpbnRzIHRoZSBjb250ZW50cyBvZiB0aGUgc3lub3BzaXMgY2hhcHRlciBvZiB0aGUgZW1iZWRkZWQgTWFya2Rvd24tZm9ybWF0dGVkIG1hbi1wYWdlIHNvdXJjZSBmb3IgcXVpY2sgcmVmZXJlbmNlLgpwcmludFVzYWdlKCkgewogIGxvY2FsIGVtYmVkZGVkVGV4dAogICMgRXh0cmFjdCB1c2FnZSBpbmZvcm1hdGlvbiBmcm9tIHRoZSBTWU5PUFNJUyBjaGFwdGVyIG9mIHRoZSBlbWJlZGRlZCBNYXJrZG93bi1mb3JtYXR0ZWQgbWFuLXBhZ2Ugc291cmNlLgogIGVtYmVkZGVkVGV4dD0kKC91c3IvYmluL3NlZCAtbiAtZSAkJy9eOiA8PFwnRU9GX01BTl9QQUdFXCcvLC9eRU9GX01BTl9QQUdFLyFkOyAvXiMjIFNZTk9QU0lTJC8sL14jL3sgcy8vLzsgdFxucDsgfScgIiRCQVNIX1NPVVJDRSIpCiAgaWYgW1sgLW4gJGVtYmVkZGVkVGV4dCBdXTsgdGhlbgogICAgIyBQcmludCBleHRyYWN0ZWQgc3lub3BzaXMgY2hhcHRlciAtIHJlbW92ZSBiYWNrdGlja3MgZm9yIHVuY2x1dHRlcmVkIGRpc3BsYXkuCiAgICBwcmludGYgJyVzXG5cbicgIiRlbWJlZGRlZFRleHQiIHwgdHIgLWQgJ2AnCiAgZWxzZSAjIE5vIFNZTk9QSVMgY2hhcHRlciBmb3VuZDsgZmFsbCBiYWNrIHRvIGRpc3BsYXlpbmcgdGhlIG1hbiBwYWdlLgogICAgZWNobyAiV0FSTklORzogdXNhZ2UgaW5mb3JtYXRpb24gbm90IGZvdW5kOyBvcGVuaW5nIG1hbiBwYWdlIGluc3RlYWQuIiA+JjIKICAgIG9wZW5NYW5QYWdlCiAgZmkKfQoKIyAtLS0gRW5kOiBTVEFOREFSRCBIRUxQRVIgRlVOQ1RJT05TCgojIC0tLSAgUFJPQ0VTUyBTVEFOREFSRCwgT1VUUFVULUlORk8tVEhFTi1FWElUIE9QVElPTlMuCmNhc2UgJDEgaW4KICAtLXZlcnNpb24pCiAgICAjIE91dHB1dCB2ZXJzaW9uIG51bWJlciBhbmQgZXhpdCwgaWYgcmVxdWVzdGVkLgogICAgdmVyPSJ2MC4zLjEiOyBlY2hvICIka1RISVNfTkFNRSAka1RISVNfVkVSU0lPTiIkJ1xuRm9yIGxpY2Vuc2UgaW5mb3JtYXRpb24gYW5kIG1vcmUsIHZpc2l0ICciJGtUSElTX0hPTUVQQUdFIjsgZXhpdCAwCiAgICA7OwogIC1ofC0taGVscCkKICAgICMgUHJpbnQgdXNhZ2UgaW5mb3JtYXRpb24gYW5kIGV4aXQuCiAgICBwcmludFVzYWdlOyBleGl0CiAgICA7OwogIC0tbWFuKQogICAgIyBEaXNwbGF5IHRoZSBtYW51YWwgcGFnZSBhbmQgZXhpdC4KICAgIG9wZW5NYW5QYWdlOyBleGl0CiAgICA7OwogIC0tbWFuLXNvdXJjZSkgIyBwcml2YXRlIG9wdGlvbiwgdXNlZCBieSBgbWFrZSB1cGRhdGUtZG9jYAogICAgIyBQcmludCByYXcsIGVtYmVkZGVkIE1hcmtkb3duLWZvcm1hdHRlZCBtYW4tcGFnZSBzb3VyY2UgYW5kIGV4aXQKICAgIHByaW50TWFuUGFnZVNvdXJjZTsgZXhpdAogICAgOzsKICAtLWhvbWUpCiAgICAjIE9wZW4gdGhlIGhvbWUgcGFnZSBhbmQgZXhpdC4KICAgIG9wZW5VcmwgIiRrVEhJU19IT01FUEFHRSI7IGV4aXQKICAgIDs7CmVzYWMKCiMgLS0tIEJlZ2luOiBTUEVDSUZJQyBIRUxQRVIgRlVOQ1RJT05TCgojIE5PVEU6IFRoZSBmdW5jdGlvbnMgYmVsb3cgb3BlcmF0ZSBvbiBieXRlIHN0cmluZ3Mgc3VjaCBhcyB0aGUgb25lIGFib3ZlOgojICAgICAgIEEgc2luZ2xlIHNpbmdsZSBzdHJpbmcgb2YgcGFpcnMgb2YgaGV4IGRpZ2l0cywgd2l0aG91dCBzZXBhcmF0b3JzIG9yIGxpbmUgYnJlYWtzLgojICAgICAgIFRodXMsIGEgZ2l2ZW4gYnl0ZSBwb3NpdGlvbiBpcyBlYXNpbHkgY2FsY3VsYXRlZDogdG8gZ2V0IGJ5dGUgJGJ5dGVJbmRleCwgdXNlCiMgICAgICAgICAke2J5dGVTdHJpbmc6Ynl0ZUluZGV4KjI6Mn0KCiMgT3V0cHV0cyB0aGUgc3BlY2lmaWVkIEVYVEVOREVEIEFUVFJJQlVURSBWQUxVRSBhcyBhIGJ5dGUgc3RyaW5nIChhIGhleCBkdW1wIHRoYXQgaXMgYSBzaW5nbGUtbGluZSBzdHJpbmcgb2YgcGFpcnMgb2YgaGV4IGRpZ2l0cywgd2l0aG91dCBzZXBhcmF0b3JzIG9yIGxpbmUgYnJlYWtzLCBzdWNoIGFzICIwMDBBMkMiLgojIElNUE9SVEFOVDogSGV4LiBkaWdpdHMgPiA5IHVzZSBVUFBQRVJDQVNFIGNoYXJhY3RlcnMuCiMgICBnZXRBdHRyaWJCeXRlU3RyaW5nIDxmaWxlPiA8YXR0cmliX25hbWU+CmdldEF0dHJpYkJ5dGVTdHJpbmcoKSB7CiAgeGF0dHIgLXB4ICIkMiIgIiQxIiB8IHRyIC1kICcgXG4nCiAgcmV0dXJuICR7UElQRVNUQVRVU1swXX0KfQoKIyBPdXRwdXRzIHRoZSBzcGVjaWZpZWQgZmlsZSdzIFJFU09VUkNFIEZPUksgYXMgYSBieXRlIHN0cmluZyAoYSBoZXggZHVtcCB0aGF0IGlzIGEgc2luZ2xlLWxpbmUgc3RyaW5nIG9mIHBhaXJzIG9mIGhleCBkaWdpdHMsIHdpdGhvdXQgc2VwYXJhdG9ycyBvciBsaW5lIGJyZWFrcywgc3VjaCBhcyAiMDAwYTJjIi4KIyBJTVBPUlRBTlQ6IEhleC4gZGlnaXRzID4gOSB1c2UgKmxvd2VyY2FzZSogY2hhcmFjdGVycy4KIyBOb3RlOiBUaGlzIGZ1bmN0aW9uIHJlbGllcyBvbiBgeHhkIC1wIDxmaWxlPi8uLm5hbWVkZm9yay9yc3JjIHwgdHIgLWQgJ1xuJ2AgcmF0aGVyIHRoYW4gdGhlIGNvbmNlcHR1YWxseSBlcXVpdmFsZW50IGNhbGwsCiMgICAgICAgYGdldEF0dHJpYkJ5dGVTdHJpbmcgPGZpbGU+IGNvbS5hcHBsZS5SZXNvdXJjZUZvcmtgLCBmb3IgUEVSRk9STUFOQ0UgcmVhc29uczogCiMgICAgICAgZ2V0QXR0cmliQnl0ZVN0cmluZygpIChkZWZpbmVkIGFib3ZlKSByZWxpZXMgb24gYHhhdHRyYCwgd2hpY2ggaXMgYSAqUHl0aG9uKiBzY3JpcHQgWyEhIHNlZW1pbmdseSBubyBsb25nZXIsIGFzIG9mIG1hY09TIDEwLjE2XSAKIyAgICAgICBhbmQgdGhlcmVmb3JlIHF1aXRlIHNsb3cgZHVlIHRvIFB5dGhvbidzIHN0YXJ0dXAgY29zdC4KIyAgIGdldFJlc291cmNlQnl0ZVN0cmluZyA8ZmlsZT4KZ2V0UmVzb3VyY2VCeXRlU3RyaW5nKCkgewogIHh4ZCAtcCAiJDEiLy4ubmFtZWRmb3JrL3JzcmMgfCB0ciAtZCAnXG4nCn0KCiMgUGF0Y2hlcyBhIHNpbmdsZSBieXRlIGluIHRoZSBieXRlIHN0cmluZyBwcm92aWRlZCB2aWEgc3RkaW4uCiMgIHBhdGNoQnl0ZUluQnl0ZVN0cmluZyBuZHggYnl0ZVNwZWMKIyAgIG5keCBpcyB0aGUgMC1iYXNlZCBieXRlIGluZGV4CiMgLSBJZiA8Ynl0ZVNwZWM+IGhhcyBOTyBwcmVmaXg6IDxieXRlU3BlYz4gYmVjb21lcyB0aGUgbmV3IGJ5dGUKIyAtIElmIDxieXRlU3BlYz4gaGFzIHByZWZpeCAnfCc6ICJhZGRzIiB0aGUgdmFsdWU6IHRoZSByZXN1bHQgb2YgYSBiaXR3aXNlIE9SIHdpdGggdGhlIGV4aXN0aW5nIGJ5dGUgYmVjb21lcyB0aGUgbmV3IGJ5dGUKIyAtIElmIDxieXRlU3BlYz4gaGFzIHByZWZpeCAnfic6ICJyZW1vdmVzIiB0aGUgdmFsdWU6IHRoZSByZXN1bHQgb2YgYSBhcHBseWluZyBhIGJpdHdpc2UgQU5EIHdpdGggdGhlIGJpdHdpc2UgY29tcGxlbWVudCBvZiA8Ynl0ZVNwZWM+IHRvIHRoZSBleGlzdGluZyBieXRlIGJlY29tZXMgdGhlIG5ldyBieXRlCnBhdGNoQnl0ZUluQnl0ZVN0cmluZygpIHsKICBsb2NhbCBuZHg9JDEgYnl0ZVNwZWM9JDIgYnl0ZVZhbCBieXRlU3RyIGNoYXJQb3Mgb3A9JycgY2hhcnNCZWZvcmU9JycgY2hhcnNBZnRlcj0nJyBjdXJyQnl0ZQogIGJ5dGVTdHI9JCg8L2Rldi9zdGRpbikKICBjaGFyUG9zPSQoKCAyICogbmR4ICkpCiAgIyBWYWxpZGF0IHRoZSBieXRlIHNwZWMuCiAgY2FzZSAke2J5dGVTcGVjOjA6MX0gaW4KICAgICd8JykKICAgICAgb3A9J3wnCiAgICAgIGJ5dGVWYWw9JHtieXRlU3BlYzoxfQogICAgICA7OwogICAgJ34nKQogICAgICBvcD0nJiB+JwogICAgICBieXRlVmFsPSR7Ynl0ZVNwZWM6MX0KICAgICAgOzsKICAgICopCiAgICAgIGJ5dGVWYWw9JGJ5dGVTcGVjCiAgICAgIDs7CiAgZXNhYwogIFtbICRieXRlVmFsID09IFswLTlBLUZhLWZdWzAtOUEtRmEtZl0gXV0gfHwgcmV0dXJuIDEKICAjIFZhbGlkYXQgdGhlIGJ5dGUgaW5kZXguCiAgKCggY2hhclBvcyA+IDAgJiYgY2hhclBvcyA8ICR7I2J5dGVTdHJ9ICkpIHx8IHJldHVybiAxCiAgIyBEZXRlcm1pbmUgdGhlIHRhcmdldCBieXRlLCBhbmQgc3RyaW5ncyBiZWZvcmUgYW5kIGFmdGVyIHRoZSBieXRlIHRvIHBhdGNoLgogICgoIGNoYXJQb3MgPj0gMiApKSAmJiBjaGFyc0JlZm9yZT0ke2J5dGVTdHI6MDpjaGFyUG9zfQogIGNoYXJzQWZ0ZXI9JHtieXRlU3RyOmNoYXJQb3MgKyAyfQogICMgRGV0ZXJtaW5lIHRoZSBuZXcgYnl0ZSB2YWx1ZQogIGlmIFtbIC1uICRvcCBdXTsgdGhlbgogICAgICBjdXJyQnl0ZT0ke2J5dGVTdHI6Y2hhclBvczoyfQogICAgICBwcmludGYgLXYgcGF0Y2hlZEJ5dGUgJyUwMlgnICIkKCggMHgke2N1cnJCeXRlfSAkb3AgMHgke2J5dGVWYWx9ICkpIgogIGVsc2UKICAgICAgcGF0Y2hlZEJ5dGU9JGJ5dGVTcGVjCiAgZmkKICBwcmludGYgJyVzJXMlcycgIiRjaGFyc0JlZm9yZSIgIiRwYXRjaGVkQnl0ZSIgIiRjaGFyc0FmdGVyIgp9CgojICBoYXNBdHRyaWIgPGZpbGVPckZvbGRlcj4gPGF0dHJpYl9uYW1lPgpoYXNBdHRyaWIoKSB7CiAgeGF0dHIgIiQxIiB8IC91c3IvYmluL2dyZXAgLUZxeCAiJDIiCn0KCiMgIGhhc0ljb25zUmVzb3VyY2UgPGZpbGU+Cmhhc0ljb25zUmVzb3VyY2UoKSB7CiAgbG9jYWwgZmlsZT0kMQogIGdldFJlc291cmNlQnl0ZVN0cmluZyAiJGZpbGUiIHwgL3Vzci9iaW4vZ3JlcCAtRnEgIiRrTUFHSUNCWVRFU19JQ05TX1JFU09VUkNFIgp9CgoKIyAgc2V0Q3VzdG9tSWNvbiA8ZmlsZU9yRm9sZGVyPiA8aW1nRmlsZT4Kc2V0Q3VzdG9tSWNvbigpIHsKCiAgbG9jYWwgZmlsZU9yRm9sZGVyPSQxIGltZ0ZpbGU9JDIKCiAgW1sgKC1mICRmaWxlT3JGb2xkZXIgfHwgLWQgJGZpbGVPckZvbGRlcikgJiYgLXIgJGZpbGVPckZvbGRlciAmJiAtdyAkZmlsZU9yRm9sZGVyIF1dIHx8IHJldHVybiAzCiAgW1sgLWYgJGltZ0ZpbGUgXV0gfHwgcmV0dXJuIDMKCiAgIyAhISBTYWRseSwgQXBwbGUgZGVjaWRlZCB0byByZW1vdmUgdGhlIGAtaWAgLyBgLS1hZGRpY29uYCBvcHRpb24gZnJvbSB0aGUgYHNpcHNgIHV0aWxpdHkuCiAgIyAhISBUaGVyZWZvcmUsIHVzZSBvZiAqQ29jb2EqIGlzIHJlcXVpcmVkLCB3aGljaCB3ZSBkbyAqdmlhIEFwcGxlU2NyaXB0KiBhbmQgaXRzIE9iakMgYnJpZGdlLAogICMgISEgd2hpY2ggaGFzIHRoZSBhZGRlZCBhZHZhbnRhZ2Ugb2YgY3JlYXRpbmcgYSAqc2V0KiBvZiBpY29ucyBmcm9tIHRoZSBzb3VyY2UgaW1hZ2UsIHNjYWxpbmcgYXMgbmVjZXNzYXJ5CiAgIyAhISAgdG8gY3JlYXRlIGEgNTEyIHggNTEyIHRvcCByZXNvbHV0aW9uIGljb24gKHdoZXJlYXMgc2lwcyAtaSBjcmVhdGVkIGEgc2luZ2xlLCAxMjggeCAxMjggaWNvbikuCiAgIyAhISBUaGFua3M6CiAgIyAhISAgKiBodHRwczovL2FwcGxlLnN0YWNrZXhjaGFuZ2UuY29tL2EvMTYxOTg0LzI4NjY4IChQeXRob24gb3JpZ2luYWwpCiAgIyAhISAgKiBAc2NyaXB0aW5nb3N4IChodHRwczovL2dpdGh1Yi5jb20vbWtsZW1lbnQwL2ZpbGVpY29uL2lzc3Vlcy8zMiNpc3N1ZWNvbW1lbnQtMTA3NDEyNDc0OCkgKEFwcGxlU2NyaXB0LU9iakMgdmVyc2lvbikKICAjICEhIE5vdGU6IFdlIG1vdmVkIGZyb20gUHl0aG9uIHRvIEFwcGxlU2NyaXB0IHdoZW4gdGhlIHN5c3RlbSBQeXRob24gd2FzIHJlbW92ZWQgaW4gbWFjT1MgMTIuMwoKICAjIFRpcHMgZm9yIGRlYnVnZ2luZzoKICAjICAqIFRvIGV4ZXJjaXNlIHRoaXMgZnVuY3Rpb24sIGZyb20gdGhlIHJlcG8gZGlyLjoKICAjICAgICAgdG91Y2ggL3RtcC90ZjsgLi9iaW4vZmlsZWljb24gc2V0IC90bXAvdGYgLi90ZXN0Ly5maXh0dXJlcy9pbWcucG5nCgogICMgISEgTm90ZTogVGhlIHNldEljb24gbWV0aG9kIHNlZW1pbmdseSBhbHdheXMgaW5kaWNhdGVzIFRydWUsIGV2ZW4gd2l0aCBpbnZhbGlkIGltYWdlIGZpbGVzLCBzbwogICMgISEgICAgICAgd2UgYXR0ZW1wdCBubyBlcnJvciBoYW5kbGluZyBpbiB0aGUgQXBwbGVTY3JpcHQgY29kZSwgYW5kIGluc3RlYWQgdmVyaWZ5IHN1Y2Nlc3MgZXhwbGljaXRseSBsYXRlci4KICBvc2FzY3JpcHQgPDxFT0YgPi9kZXYvbnVsbCB8fCBkaWUKICAgIHVzZSBmcmFtZXdvcmsgIkNvY29hIgoKICAgIHNldCBzb3VyY2VQYXRoIHRvICIkaW1nRmlsZSIKICAgIHNldCBkZXN0UGF0aCB0byAiJGZpbGVPckZvbGRlciIKCiAgICBzZXQgaW1hZ2VEYXRhIHRvIChjdXJyZW50IGFwcGxpY2F0aW9uJ3MgTlNJbWFnZSdzIGFsbG9jKCkncyBpbml0V2l0aENvbnRlbnRzT2ZGaWxlOnNvdXJjZVBhdGgpCiAgICAoY3VycmVudCBhcHBsaWNhdGlvbidzIE5TV29ya3NwYWNlJ3Mgc2hhcmVkV29ya3NwYWNlKCkncyBzZXRJY29uOmltYWdlRGF0YSBmb3JGaWxlOmRlc3RQYXRoIG9wdGlvbnM6MikKRU9GCgogICMgVmVyaWZ5IHRoYXQgYSByZXNvdXJjZSBmb3JrIHdpdGggaWNvbnMgd2FzIGFjdHVhbGx5IGNyZWF0ZWQuCiAgIyBGb3IgKmZpbGVzKiwgdGhlIHJlc291cmNlIGZvcmsgaXMgZW1iZWRkZWQgaW4gdGhlIGZpbGUgaXRzZWxmLgogICMgRm9yICpmb2xkZXJzKiBhIGhpZGRlbiBmaWxlIG5hbWVkICQnSWNvblxyJyBpcyBjcmVhdGVkICppbnNpZGUgdGhlIGZvbGRlciouCiAgW1sgLWQgJGZpbGVPckZvbGRlciBdXSAmJiBmaWxlV2l0aFJlc291cmNlRm9yaz0ke2ZpbGVPckZvbGRlcn0vJGtGSUxFTkFNRV9GT0xERVJDVVNUT01JQ09OIHx8IGZpbGVXaXRoUmVzb3VyY2VGb3JrPSRmaWxlT3JGb2xkZXIKICBoYXNJY29uc1Jlc291cmNlICIkZmlsZVdpdGhSZXNvdXJjZUZvcmsiIHx8IHsgCiAgICBjYXQgPiYyIDw8RU9GCkZhaWxlZCB0byBjcmVhdGUgcmVzb3VyY2UgZm9yayB3aXRoIGljb25zLiBUeXBpY2FsbHksIHRoaXMgbWVhbnMgdGhhdCB0aGUgc3BlY2lmaWVkIGltYWdlIGZpbGUgaXMgbm90IHN1cHBvcnRlZCBvciBjb3JydXB0OiAkaW1nRmlsZQpTdXBwb3J0ZWQgaW1hZ2UgZm9ybWF0czoganBlZyB8IHRpZmYgfCBwbmcgfCBnaWYgfCBqcDIgfCBwaWN0IHwgYm1wIHwgcXRpZnwgcHNkIHwgc2dpIHwgdGdhCkVPRgogICAgcmV0dXJuIDEKCiAgfQoKICByZXR1cm4gMAp9CgojICBnZXRDdXN0b21JY29uIDxmaWxlT3JGb2xkZXI+IDxpY25zT3V0RmlsZT4KZ2V0Q3VzdG9tSWNvbigpIHsKCiAgbG9jYWwgZmlsZU9yRm9sZGVyPSQxIGljbnNPdXRGaWxlPSQyIGJ5dGVTdHIgZmlsZVdpdGhSZXNvdXJjZUZvcmsgYnl0ZU9mZnNldCBieXRlQ291bnQKCiAgW1sgKC1mICRmaWxlT3JGb2xkZXIgfHwgLWQgJGZpbGVPckZvbGRlcikgJiYgLXIgJGZpbGVPckZvbGRlciBdXSB8fCByZXR1cm4gMwoKICAjIERldGVybWluZSB3aGF0IGZpbGUgdG8gZXh0cmFjdCB0aGUgcmVzb3VyY2UgZm9yayBmcm9tLgogIGlmIFtbIC1kICRmaWxlT3JGb2xkZXIgXV07IHRoZW4KICAgIGZpbGVXaXRoUmVzb3VyY2VGb3JrPSR7ZmlsZU9yRm9sZGVyfS8ka0ZJTEVOQU1FX0ZPTERFUkNVU1RPTUlDT04KICAgIFtbIC1mICRmaWxlV2l0aFJlc291cmNlRm9yayBdXSB8fCB7IGVjaG8gIkN1c3RvbS1pY29uIGZpbGUgZG9lcyBub3QgZXhpc3Q6ICcke2ZpbGVXaXRoUmVzb3VyY2VGb3JrLyQnXHInL1xccn0nIiA+JjI7IHJldHVybiAxOyB9CiAgZWxzZQogICAgZmlsZVdpdGhSZXNvdXJjZUZvcms9JGZpbGVPckZvbGRlcgogIGZpCgogICMgRGV0ZXJtaW5lIChiYXNlZCBvbiBmb3JtYXQgZGVzY3JpcHRpb24gYXQgaHR0cHM6Ly9lbi53aWtpcGVkaWEub3JnL3dpa2kvQXBwbGVfSWNvbl9JbWFnZV9mb3JtYXQpOgogICMgLSB0aGUgYnl0ZSBvZmZzZXQgYXQgd2hpY2ggdGhlIGljbnMgcmVzb3VyY2UgYmVnaW5zLCB2aWEgdGhlIG1hZ2ljIGxpdGVyYWwgaWRlbnRpZnlpbmcgYW4gaWNucyByZXNvdXJjZQogICMgLSB0aGUgbGVuZ3RoIG9mIHRoZSByZXNvdXJjZSwgd2hpY2ggaXMgZW5jb2RlZCBpbiB0aGUgNCBieXRlcyByaWdodCBhZnRlciB0aGUgbWFnaWMgbGl0ZXJhbC4KICByZWFkIC1yIGJ5dGVPZmZzZXQgYnl0ZUNvdW50IDwgPChnZXRSZXNvdXJjZUJ5dGVTdHJpbmcgIiRmaWxlV2l0aFJlc291cmNlRm9yayIgfCAvdXNyL2Jpbi9hd2sgLUYgIiRrTUFHSUNCWVRFU19JQ05TX1JFU09VUkNFIiAneyBwcmludGYgIiVzICVkIiwgKGxlbmd0aCgkMSkgKyAyKSAvIDIsICIweCIgc3Vic3RyKCQyLCAwLCA4KSB9JykKICAoKCBieXRlT2Zmc2V0ID4gMCAmJiBieXRlQ291bnQgPiAwICkpIHx8IHsgZWNobyAiQ3VzdG9tLWljb24gZmlsZSBjb250YWlucyBubyBpY29ucyByZXNvdXJjZTogJyR7ZmlsZVdpdGhSZXNvdXJjZUZvcmsvJCdccicvXFxyfSciID4mMjsgcmV0dXJuIDE7IH0KCiAgIyBFeHRyYWN0IHRoZSBhY3R1YWwgYnl0ZXMgdXNpbmcgdGFpbCBhbmQgaGVhZCBhbmQgc2F2ZSB0aGVtIHRvIHRoZSBvdXRwdXQgZmlsZS4KICB0YWlsIC1jICIrJHtieXRlT2Zmc2V0fSIgIiRmaWxlV2l0aFJlc291cmNlRm9yay8uLm5hbWVkZm9yay9yc3JjIiB8IGhlYWQgLWMgJGJ5dGVDb3VudCA+ICIkaWNuc091dEZpbGUiIHx8IHJldHVybgoKICByZXR1cm4gMAp9CgojICByZW1vdmVDdXN0b21JY29uIDxmaWxlT3JGb2xkZXI+CnJlbW92ZUN1c3RvbUljb24oKSB7CgogIGxvY2FsIGZpbGVPckZvbGRlcj0kMSBieXRlU3RyCgogIFtbICgtZiAkZmlsZU9yRm9sZGVyIHx8IC1kICRmaWxlT3JGb2xkZXIpICYmIC1yICRmaWxlT3JGb2xkZXIgJiYgLXcgJGZpbGVPckZvbGRlciBdXSB8fCByZXR1cm4gMQoKICAjIFN0ZXAgMTogVHVybiBvZmYgdGhlIGN1c3RvbS1pY29uIGZsYWcgaW4gdGhlIGNvbS5hcHBsZS5GaW5kZXJJbmZvIGV4dGVuZGVkIGF0dHJpYnV0ZS4KICBpZiBoYXNBdHRyaWIgIiRmaWxlT3JGb2xkZXIiIGNvbS5hcHBsZS5GaW5kZXJJbmZvOyB0aGVuCiAgICBieXRlU3RyPSQoZ2V0QXR0cmliQnl0ZVN0cmluZyAiJGZpbGVPckZvbGRlciIgY29tLmFwcGxlLkZpbmRlckluZm8gfCBwYXRjaEJ5dGVJbkJ5dGVTdHJpbmcgJGtGSV9CWVRFT0ZGU0VUX0NVU1RPTUlDT04gJ34nJGtGSV9WQUxfQ1VTVE9NSUNPTikgfHwgcmV0dXJuCiAgICBpZiBbWyAkYnl0ZVN0ciA9PSAiJGtGSV9CWVRFU19CTEFOSyIgXV07IHRoZW4gIyBBbGwgYnl0ZXMgY2xlYXJlZD8gUmVtb3ZlIHRoZSBlbnRpcmUgYXR0cmlidXRlLgogICAgICB4YXR0ciAtZCBjb20uYXBwbGUuRmluZGVySW5mbyAiJGZpbGVPckZvbGRlciIKICAgIGVsc2UgIyBVcGRhdGUgdGhlIGF0dHJpYnV0ZS4KICAgICAgeGF0dHIgLXd4IGNvbS5hcHBsZS5GaW5kZXJJbmZvICIkYnl0ZVN0ciIgIiRmaWxlT3JGb2xkZXIiIHx8IHJldHVybgogICAgZmkKICBmaQoKICAjIFN0ZXAgMjogUmVtb3ZlIHRoZSByZXNvdXJjZSBmb3JrIChpZiB0YXJnZXQgaXMgYSBmaWxlKSAvIGhpZGRlbiBmaWxlIHdpdGggY3VzdG9tIGljb24gKGlmIHRhcmdldCBpcyBhIGZvbGRlcikKICBpZiBbWyAtZCAkZmlsZU9yRm9sZGVyIF1dOyB0aGVuCiAgICBybSAtZiAiJHtmaWxlT3JGb2xkZXJ9LyR7a0ZJTEVOQU1FX0ZPTERFUkNVU1RPTUlDT059IgogIGVsc2UKICAgIGlmIGhhc0ljb25zUmVzb3VyY2UgIiRmaWxlT3JGb2xkZXIiOyB0aGVuCiAgICAgIHhhdHRyIC1kIGNvbS5hcHBsZS5SZXNvdXJjZUZvcmsgIiRmaWxlT3JGb2xkZXIiCiAgICBmaQogIGZpCgogIHJldHVybiAwCn0KCiMgIHRlc3RGb3JDdXN0b21JY29uIDxmaWxlT3JGb2xkZXI+CnRlc3RGb3JDdXN0b21JY29uKCkgewoKICBsb2NhbCBmaWxlT3JGb2xkZXI9JDEgYnl0ZVN0ciBieXRlVmFsIGZpbGVXaXRoUmVzb3VyY2VGb3JrCgogIFtbICgtZiAkZmlsZU9yRm9sZGVyIHx8IC1kICRmaWxlT3JGb2xkZXIpICYmIC1yICRmaWxlT3JGb2xkZXIgXV0gfHwgcmV0dXJuIDMKCiAgIyBTdGVwIDE6IENoZWNrIGlmIHRoZSBjb20uYXBwbGUuRmluZGVySW5mbyBleHRlbmRlZCBhdHRyaWJ1dGUgaGFzIHRoZSBjdXN0b20taWNvbgogICMgICAgICAgICBmbGFnIHNldC4KICBieXRlU3RyPSQoZ2V0QXR0cmliQnl0ZVN0cmluZyAiJGZpbGVPckZvbGRlciIgY29tLmFwcGxlLkZpbmRlckluZm8gMj4vZGV2L251bGwpIHx8IHJldHVybiAxCgogIGJ5dGVWYWw9JHtieXRlU3RyOjIqa0ZJX0JZVEVPRkZTRVRfQ1VTVE9NSUNPTjoyfQoKICAoKCBieXRlVmFsICYga0ZJX1ZBTF9DVVNUT01JQ09OICkpIHx8IHJldHVybiAxCgogICMgU3RlcCAyOiBDaGVjayBpZiB0aGUgcmVzb3VyY2UgZm9yayBvZiB0aGUgcmVsZXZhbnQgZmlsZSBjb250YWlucyBhbiBpY25zIHJlc291cmNlCiAgaWYgW1sgLWQgJGZpbGVPckZvbGRlciBdXTsgdGhlbgogICAgZmlsZVdpdGhSZXNvdXJjZUZvcms9JHtmaWxlT3JGb2xkZXJ9LyR7a0ZJTEVOQU1FX0ZPTERFUkNVU1RPTUlDT059CiAgZWxzZQogICAgZmlsZVdpdGhSZXNvdXJjZUZvcms9JGZpbGVPckZvbGRlcgogIGZpCgogIGhhc0ljb25zUmVzb3VyY2UgIiRmaWxlV2l0aFJlc291cmNlRm9yayIgfHwgcmV0dXJuIDEKCiAgcmV0dXJuIDAKfQoKIyAtLS0gRW5kOiBTUEVDSUZJQyBIRUxQRVIgRlVOQ1RJT05TCgojIC0tLSBCZWdpbjogU1BFQ0lGSUMgU0NSSVBULUdMT0JBTCBDT05TVEFOVFMKCmtGSUxFTkFNRV9GT0xERVJDVVNUT01JQ09OPSQnSWNvblxyJwoKIyBUaGUgYmxhbmsgaGV4IGR1bXAgZm9ybSAoc2luZ2xlIHN0cmluZyBvZiBwYWlycyBvZiBoZXggZGlnaXRzKSBvZiB0aGUgMzItYnl0ZSBkYXRhIHN0cnVjdHVyZSBzdG9yZWQgaW4gZXh0ZW5kZWQgYXR0cmlidXRlCiMgY29tLmFwcGxlLkZpbmRlckluZm8Ka0ZJX0JZVEVTX0JMQU5LPScwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwJwoKIyBUaGUgaGV4IGR1bXAgZm9ybSBvZiB0aGUgZnVsbCAzMiBieXRlcyB0aGF0IEZpbmRlciBhc3NpZ25zIHRvIHRoZSBoaWRkZW4gJCdJY29uXHInCiMgZmlsZSB3aG9zZSBjb20uYXBwbGUuUmVzb3VyY2VGb3JrIGV4dGVuZGVkIGF0dHJpYnV0ZSBjb250YWlucyB0aGUgaWNvbiBpbWFnZSBkYXRhIGZvciB0aGUgZW5jbG9zaW5nIGZvbGRlci4KIyBUaGUgZmlyc3QgOCBieXRlcyBzcGVsbCBvdXQgdGhlIG1hZ2ljIGxpdGVyYWwgJ2ljb25NQUNTJzsgdGhleSBhcmUgZm9sbG93ZWQgYnkgdGhlIGludmlzaWJpbGl0eSBmbGFnLCAnNDAnIGluIHRoZSA5dGggYnl0ZSwgYW5kICcxMCcgKD8/IHNwZWNpZnlpbmcgd2hhdD8pCiMgaW4gdGhlIDEwdGggYnl0ZS4KIyBOT1RFOiBTaW5jZSBmaWxlICQnSWNvblxyJyBzZXJ2ZXMgbm8gb3RoZXIgcHVycG9zZSB0aGFuIHRvIHN0b3JlIHRoZSBpY29uLCBpdCBpcwojICAgICAgIHNhZmUgdG8gc2ltcGx5IGFzc2lnbiBhbGwgMzIgYnl0ZXMgYmxpbmRseSwgd2l0aG91dCBoYXZpbmcgdG8gd29ycnkgYWJvdXQKIyAgICAgICBwcmVzZXJ2aW5nIGV4aXN0aW5nIHZhbHVlcy4Ka0ZJX0JZVEVTX0NVU1RPTUlDT05GSUxFRk9SRk9MREVSPSc2OTYzNkY2RTRENDE0MzUzNDAxMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwJwoKIyBUaGUgaGV4IGR1bXAgZm9ybSBvZiB0aGUgbWFnaWMgbGl0ZXJhbCBpbnNpZGUgYSByZXNvdXJjZSBmb3JrIHRoYXQgbWFya3MgdGhlCiMgc3RhcnQgb2YgYW4gaWNucyAoaWNvbnMpIHJlc291cmNlLgojIE5PVEU6IFRoaXMgd2lsbCBiZSB1c2VkIHdpdGggYHh4ZCAtcCAuLiB8IHRyIC1kICdcbidgLCB3aGljaCB1c2VzICpsb3dlcmNhc2UqCiMgICAgICAgaGV4IGRpZ2l0cywgc28gd2UgbXVzdCB1c2UgbG93ZXJjYXNlIGhlcmUuCmtNQUdJQ0JZVEVTX0lDTlNfUkVTT1VSQ0U9JzY5NjM2ZTczJwoKIyBUaGUgYnl0ZSB2YWx1ZXMgKGFzIGhleCBzdHJpbmdzKSBvZiB0aGUgZmxhZ3MgYXQgdGhlIHJlbGV2YW50IGJ5dGUgcG9zaXRpb24KIyBvZiB0aGUgY29tLmFwcGxlLkZpbmRlckluZm8gZXh0ZW5kZWQgYXR0cmlidXRlLgprRklfVkFMX0NVU1RPTUlDT049JzA0JwoKIyBUaGUgY3VzdG9tLWljb24tZmxhZyBieXRlIG9mZnNldCBpbiB0aGUgY29tLmFwcGxlLkZpbmRlckluZm8gZXh0ZW5kZWQgYXR0cmlidXRlLgprRklfQllURU9GRlNFVF9DVVNUT01JQ09OPTgKCiMgLS0tIEVuZDogU1BFQ0lGSUMgU0NSSVBULUdMT0JBTCBDT05TVEFOVFMKCiMgT3B0aW9uIGRlZmF1bHRzLgpmb3JjZT0wIHF1aWV0PTAKCiMgLS0tIEJlZ2luOiBPUFRJT05TIFBBUlNJTkcKYWxsb3dPcHRzQWZ0ZXJPcGVyYW5kcz0xIG9wZXJhbmRzPSgpIGk9MCBvcHROYW1lPSBpc0xvbmc9MCBwcmVmaXg9IG9wdEFyZz0gaGF2ZU9wdEFyZ0F0dGFjaGVkPTAgaGF2ZU9wdEFyZ0FzTmV4dEFyZz0wIGFjY2VwdE9wdEFyZz0wIG5lZWRPcHRBcmc9MAp3aGlsZSAoKCAkIyApKTsgZG8KICBpZiBbWyAkMSA9fiBeKC0pW2EtekEtWjAtOV0rLiokIHx8ICQxID1+IF4oLS0pW2EtekEtWjAtOV0rLiokIF1dOyB0aGVuICMgYW4gb3B0aW9uOiBlaXRoZXIgYSBzaG9ydCBvcHRpb24gLyBtdWx0aXBsZSBzaG9ydCBvcHRpb25zIGluIGNvbXByZXNzZWQgZm9ybSBvciBhIGxvbmcgb3B0aW9uCiAgICBwcmVmaXg9JHtCQVNIX1JFTUFUQ0hbMV19OyBbWyAkcHJlZml4ID09ICctLScgXV0gJiYgaXNMb25nPTEgfHwgaXNMb25nPTAKICAgIGZvciAoKCBpID0gMTsgaSA8IChpc0xvbmcgPyAyIDogJHsjMX0pOyBpKysgKSk7IGRvCiAgICAgICAgYWNjZXB0T3B0QXJnPTAgbmVlZE9wdEFyZz0wIGhhdmVPcHRBcmdBdHRhY2hlZD0wIGhhdmVPcHRBcmdBc05leHRBcmc9MCBvcHRBcmdBdHRhY2hlZD0gb3B0QXJnT3B0PSBvcHRBcmdSZXE9CiAgICAgICAgaWYgKCggaXNMb25nICkpOyB0aGVuICMgbG9uZyBvcHRpb246IHBhcnNlIGludG8gbmFtZSBhbmQsIGlmIHByZXNlbnQsIGFyZ3VtZW50CiAgICAgICAgICBvcHROYW1lPSR7MToyfQogICAgICAgICAgW1sgJG9wdE5hbWUgPX4gXihbXj1dKyk9KC4qKSQgXV0gJiYgeyBvcHROYW1lPSR7QkFTSF9SRU1BVENIWzFdfTsgb3B0QXJnQXR0YWNoZWQ9JHtCQVNIX1JFTUFUQ0hbMl19OyBoYXZlT3B0QXJnQXR0YWNoZWQ9MTsgfQogICAgICAgIGVsc2UgIyBzaG9ydCBvcHRpb246ICppZiogaXQgdGFrZXMgYW4gYXJndW1lbnQsIHRoZSByZXN0IG9mIHRoZSBzdHJpbmcsIGlmIGFueSwgaXMgYnkgZGVmaW5pdGlvbiB0aGUgYXJndW1lbnQuCiAgICAgICAgICBvcHROYW1lPSR7MTppOjF9OyBvcHRBcmdBdHRhY2hlZD0kezE6aSsxfTsgKCggJHsjb3B0QXJnQXR0YWNoZWR9ID49IDEgKSkgJiYgaGF2ZU9wdEFyZ0F0dGFjaGVkPTEKICAgICAgICBmaQogICAgICAgICgoIGhhdmVPcHRBcmdBdHRhY2hlZCApKSAmJiBvcHRBcmdPcHQ9JG9wdEFyZ0F0dGFjaGVkIG9wdEFyZ1JlcT0kb3B0QXJnQXR0YWNoZWQgfHwgeyAoKCAkIyA+IDEgKSkgJiYgeyBvcHRBcmdSZXE9JDI7IGhhdmVPcHRBcmdBc05leHRBcmc9MTsgfTsgfQogICAgICAgICMgLS0tLSBCRUdJTjogQ1VTVE9NSVpFIEhFUkUKICAgICAgICBjYXNlICRvcHROYW1lIGluCiAgICAgICAgICBmfGZvcmNlKQogICAgICAgICAgICBmb3JjZT0xCiAgICAgICAgICAgIDs7CiAgICAgICAgICBxfHF1aWV0KQogICAgICAgICAgICBxdWlldD0xCiAgICAgICAgICAgIDs7CiAgICAgICAgICAqKQogICAgICAgICAgICBkaWVTeW50YXggIlVua25vd24gb3B0aW9uOiAke3ByZWZpeH0ke29wdE5hbWV9LiIKICAgICAgICAgICAgOzsKICAgICAgICBlc2FjCiAgICAgICAgIyAtLS0tIEVORDogQ1VTVE9NSVpFIEhFUkUKICAgICAgICAoKCBuZWVkT3B0QXJnICkpICYmIHsgKCggISBoYXZlT3B0QXJnQXR0YWNoZWQgJiYgISBoYXZlT3B0QXJnQXNOZXh0QXJnICkpICYmIGRpZVN5bnRheCAiT3B0aW9uICR7cHJlZml4fSR7b3B0TmFtZX0gaXMgbWlzc2luZyBpdHMgYXJndW1lbnQuIiB8fCAoKCBoYXZlT3B0QXJnQXNOZXh0QXJnICkpICYmIHNoaWZ0OyB9CiAgICAgICAgKCggYWNjZXB0T3B0QXJnIHx8IG5lZWRPcHRBcmcgKSkgJiYgYnJlYWsKICAgIGRvbmUKICBlbHNlICMgYW4gb3BlcmFuZAogICAgaWYgW1sgJDEgPT0gJy0tJyBdXTsgdGhlbgogICAgICBzaGlmdDsgb3BlcmFuZHMrPSggIiRAIiApOyBicmVhawogICAgZWxpZiAoKCBhbGxvd09wdHNBZnRlck9wZXJhbmRzICkpOyB0aGVuCiAgICAgIG9wZXJhbmRzKz0oICIkMSIgKSAjIGNvbnRpbnVlCiAgICBlbHNlCiAgICAgIG9wZXJhbmRzPSggIiRAIiApCiAgICAgIGJyZWFrCiAgICBmaQogIGZpCiAgc2hpZnQKZG9uZQooKCAiJHsjb3BlcmFuZHNbQF19IiA+IDAgKSkgJiYgc2V0IC0tICIke29wZXJhbmRzW0BdfSI7IHVuc2V0IGFsbG93T3B0c0FmdGVyT3BlcmFuZHMgb3BlcmFuZHMgaSBvcHROYW1lIGlzTG9uZyBwcmVmaXggb3B0QXJnQXR0YWNoZWQgaGF2ZU9wdEFyZ0F0dGFjaGVkIGhhdmVPcHRBcmdBc05leHRBcmcgYWNjZXB0T3B0QXJnIG5lZWRPcHRBcmcKIyAtLS0gRW5kOiBPUFRJT05TIFBBUlNJTkc6ICIkQCIgbm93IGNvbnRhaW5zIGFsbCBvcGVyYW5kcyAobm9uLW9wdGlvbiBhcmd1bWVudHMpLgoKIyBWYWxpZGF0ZSB0aGUgY29tbWFuZApjbWQ9JChwcmludGYgJXMgIiQxIiB8IHRyICdbOnVwcGVyOl0nICdbOmxvd2VyOl0nKSAjIHRyYW5zbGF0ZSB0byBhbGwtbG93ZXJjYXNlIC0gd2UgZG9uJ3Qgd2FudCB0aGUgY29tbWFuZCBuYW1lIHRvIGJlIGNhc2Utc2Vuc2l0aXZlCltbICRjbWQgPT0gJ3JlbW92ZScgXV0gJiYgY21kPSdybScgICMgc3VwcG9ydCBhbGlhcyAncmVtb3ZlJyBmb3IgJ3JtJwpjYXNlICRjbWQgaW4KICBzZXR8Z2V0fHJtfHJlbW92ZXx0ZXN0KQogICAgc2hpZnQKICAgIDs7CiAgKikKICAgIGRpZVN5bnRheCAiVW5yZWNvZ25pemVkIG9yIG1pc3NpbmcgY29tbWFuZDogJyRjbWQnLiIKICAgIDs7CmVzYWMKCiMgVmFsaWRhdGUgZmlsZSBvcGVyYW5kcwooKCAkIyA+IDAgKSkgfHwgZGllU3ludGF4ICJNaXNzaW5nIG9wZXJhbmQocykuIgoKIyBUYXJnZXQgZmlsZSBvciBmb2xkZXIuCnRhcmdldEZpbGVPckZvbGRlcj0kMSBpbWdGaWxlPSBvdXRGaWxlPQpbWyAtZiAkdGFyZ2V0RmlsZU9yRm9sZGVyIHx8IC1kICR0YXJnZXRGaWxlT3JGb2xkZXIgXV0gfHwgZGllICJUYXJnZXQgbm90IGZvdW5kIG9yIG5laXRoZXIgZmlsZSBub3IgZm9sZGVyOiAnJHRhcmdldEZpbGVPckZvbGRlciciCiMgTWFrZSBzdXJlIHRoZSB0YXJnZXQgZmlsZS9mb2xkZXIgaXMgcmVhZGFibGUsIGFuZCwgdW5sZXNzIG9ubHkgZ2V0dGluZyBvciB0ZXN0aW5nIGZvciBhbiBpY29uIGFyZSByZXF1ZXN0ZWQsIHdyaXRlYWJsZSB0b28uCltbIC1yICR0YXJnZXRGaWxlT3JGb2xkZXIgXV0gfHwgZGllICJDYW5ub3QgYWNjZXNzICckdGFyZ2V0RmlsZU9yRm9sZGVyJzogeW91IGRvIG5vdCBoYXZlIHJlYWQgcGVybWlzc2lvbnMuIgpbWyAkY21kID09ICd0ZXN0JyB8fCAkY21kID09ICdnZXQnIHx8IC13ICR0YXJnZXRGaWxlT3JGb2xkZXIgXV0gfHwgZGllICJDYW5ub3QgbW9kaWZ5ICckdGFyZ2V0RmlsZU9yRm9sZGVyJzogeW91IGRvIG5vdCBoYXZlIHdyaXRlIHBlcm1pc3Npb25zLiIKCiMgT3RoZXIgb3BlcmFuZHMsIGlmIGFueSwgYW5kIHRoZWlyIG51bWJlci4KdmFsaWQ9MApjYXNlICRjbWQgaW4KICAnc2V0JykKICAgICgoICQjIDw9IDIgKSkgJiYgewogICAgICB2YWxpZD0xCiAgICAgICMgSWYgbm8gaW1hZ2UgZmlsZSB3YXMgc3BlY2lmaWVkLCB0aGUgdGFyZ2V0IGZpbGUgaXMgYXNzdW1lZCB0byBiZSBhbiBpbWFnZSBmaWxlIGl0c2VsZiB3aG9zZSBpbWFnZSBzaG91bGQgYmUgc2VsZi1hc3NpZ25lZCBhcyBhbiBpY29uLgogICAgICAoKCAkIyA9PSAyICkpICYmIGltZ0ZpbGU9JDIgfHwgaW1nRmlsZT0kMQogICAgICAjICEhIEFwcGFyZW50bHksIGEgcmVndWxhciBmaWxlIGlzIHJlcXVpcmVkIC0gYSBwcm9jZXNzIHN1YnNpdHV0aW9uIHN1Y2ggCiAgICAgICMgISEgYXMgYDwoYmFzZTY0IC1EIDxlbmNvZGVkLWZpbGUudHh0KWAgaXMgTk9UIHN1cHBvcnRlZCBieSBOU0ltYWdlLmluaXRXaXRoQ29udGVudHNPZkZpbGUoKQogICAgICBbWyAtZiAkaW1nRmlsZSAmJiAtciAkaW1nRmlsZSBdXSB8fCBkaWUgIkltYWdlIGZpbGUgbm90IGZvdW5kIG9yIG5vdCBhIChyZWFkYWJsZSkgcmVndWxhciBmaWxlOiAkaW1nRmlsZSIKICAgIH0KICAgIDs7CiAgJ3JtJ3wndGVzdCcpCiAgICAoKCAkIyA9PSAxICkpICYmIHZhbGlkPTEKICAgIDs7CiAgJ2dldCcpCiAgICAoKCAkIyA9PSAxIHx8ICQjID09IDIgKSkgJiYgewogICAgICB2YWxpZD0xCiAgICAgIG91dEZpbGU9JDIKICAgICAgaWYgW1sgJG91dEZpbGUgPT0gJy0nIF1dOyB0aGVuCiAgICAgICAgb3V0RmlsZT0vZGV2L3N0ZG91dAogICAgICBlbHNlCiAgICAgICAgIyBCeSBkZWZhdWx0LCB3ZSBleHRyYWN0IHRvIGEgZmlsZSB3aXRoIHRoZSBzYW1lIGZpbGVuYW1lIHJvb3QgKyAnLmljbnMnCiAgICAgICAgIyBpbiB0aGUgY3VycmVudCBmb2xkZXIuCiAgICAgICAgW1sgLXogJG91dEZpbGUgXV0gJiYgb3V0RmlsZT0ke3RhcmdldEZpbGVPckZvbGRlciMjKi99CiAgICAgICAgIyBVbmxlc3MgYWxyZWFkeSBzcGVjaWZpZWQsIHdlIGFwcGVuZCAnLmljbnMnIHRvIHRoZSBvdXRwdXQgZmlsZW5hbWUuCiAgICAgICAgbXVzdFJlc2V0PSQoc2hvcHQgLXEgbm9jYXNlbWF0Y2g7IGVjaG8gJD8pOyBzaG9wdCAtcyBub2Nhc2VtYXRjaAogICAgICAgIFtbICRvdXRGaWxlID1+IFwuaWNucyQgXV0gfHwgb3V0RmlsZSs9Jy5pY25zJwogICAgICAgICgoIG11c3RSZXNldCApKSAmJiBzaG9wdCAtdSBub2Nhc2VtYXRjaAogICAgICAgIFtbIC1lICRvdXRGaWxlICYmICRmb3JjZSAtZXEgMCBdXSAmJiBkaWUgIk91dHB1dCBmaWxlICckb3V0RmlsZScgYWxyZWFkeSBleGlzdHMuIFRvIGZvcmNlIGl0cyByZXBsYWNlbWVudCwgdXNlIC1mLiIKICAgICAgZmkKICAgIH0KICAgIDs7CmVzYWMKKCggdmFsaWQgKSkgfHwgZGllU3ludGF4ICJVbmV4cGVjdGVkIG51bWJlciBvZiBvcGVyYW5kcy4iCgpjYXNlICRjbWQgaW4KICAnc2V0JykKICAgIHNldEN1c3RvbUljb24gIiR0YXJnZXRGaWxlT3JGb2xkZXIiICIkaW1nRmlsZSIgfHwgZGllCiAgICAoKCBxdWlldCApKSB8fCBlY2hvICJDdXN0b20gaWNvbiBhc3NpZ25lZCB0byAnJHRhcmdldEZpbGVPckZvbGRlcicgYmFzZWQgb24gJyRpbWdGaWxlJy4iCiAgICA7OwogICdybScpCiAgICByZW1vdmVDdXN0b21JY29uICIkdGFyZ2V0RmlsZU9yRm9sZGVyIiB8fCBkaWUKICAgICgoIHF1aWV0ICkpIHx8IGVjaG8gIkN1c3RvbSBpY29uIHJlbW92ZWQgZnJvbSAnJHRhcmdldEZpbGVPckZvbGRlcicuIgogICAgOzsKICAnZ2V0JykKICAgIGdldEN1c3RvbUljb24gIiR0YXJnZXRGaWxlT3JGb2xkZXIiICIkb3V0RmlsZSIgfHwgZGllCiAgICAoKCBxdWlldCApKSB8fCB7IFtbICRvdXRGaWxlICE9ICcvZGV2L3N0ZG91dCcgXV0gJiYgZWNobyAiQ3VzdG9tIGljb24gZXh0cmFjdGVkIHRvICckb3V0RmlsZScuIjsgfQogICAgZXhpdCAwCiAgICA7OwogICd0ZXN0JykKICAgIHRlc3RGb3JDdXN0b21JY29uICIkdGFyZ2V0RmlsZU9yRm9sZGVyIgogICAgZWM9JD8KICAgICgoIGVjIDw9IDEgKSkgfHwgZGllCiAgICBpZiAoKCAhIHF1aWV0ICkpOyB0aGVuCiAgICAgICgoIGVjID09IDAgKSkgJiYgZWNobyAiSEFTIGN1c3RvbSBpY29uOiAnJHRhcmdldEZpbGVPckZvbGRlciciIHx8IGVjaG8gIkhhcyBOTyBjdXN0b20gaWNvbjogJyR0YXJnZXRGaWxlT3JGb2xkZXInIgogICAgZmkKICAgIGV4aXQgJGVjCiAgICA7OwogICopCiAgICBkaWUgIkRFU0lHTiBFUlJPUjogdW5hbnRpY2lwYXRlZCBjb21tYW5kOiAkY21kIgogICAgOzsKZXNhYwoKZXhpdCAwCgojIyMjCiMgTUFOIFBBR0UgTUFSS0RPV04gU09VUkNFCiMgIC0gUGxhY2UgYSBNYXJrZG93bi1mb3JtYXR0ZWQgdmVyc2lvbiBvZiB0aGUgbWFuIHBhZ2UgZm9yIHRoaXMgc2NyaXB0CiMgICAgaW5zaWRlIHRoZSBoZXJlLWRvY3VtZW50IGJlbG93LgojICAgIFRoZSBkb2N1bWVudCBtdXN0IGJlIGZvcm1hdHRlZCB0byBsb29rIGdvb2QgaW4gYWxsIDMgdmlld2luZyBzY2VuYXJpb3M6CiMgICAgIC0gYXMgYSBtYW4gcGFnZSwgYWZ0ZXIgY29udmVyc2lvbiB0byBST0ZGIHdpdGggbWFya2VkLW1hbgojICAgICAtIGFzIHBsYWluIHRleHQgKHJhdyBNYXJrZG93biBzb3VyY2UpCiMgICAgIC0gYXMgSFRNTCAocmVuZGVyZWQgTWFya2Rvd24pCiMgIE1hcmtkb3duIGZvcm1hdHRpbmcgdGlwczoKIyAgIC0gR0VORVJBTAojICAgICBUbyBzdXBwb3J0IHBsYWluLXRleHQgcmVuZGVyaW5nIGluIHRoZSB0ZXJtaW5hbCwgbGltaXQgYWxsIGxpbmVzIHRvIDgwIGNoYXJzLiwKIyAgICAgYW5kLCBmb3Igc2ltaWxhciByZW5kZXJpbmcgYXMgSFRNTCwgKmVuZCBldmVyeSBsaW5lIHdpdGggMiB0cmFpbGluZyBzcGFjZXMqLgojICAgLSBIRUFESU5HUwojICAgICAtIEZvciBiZXR0ZXIgcGxhaW4tdGV4dCByZW5kZXJpbmcsIGxlYXZlIGFuIGVtcHR5IGxpbmUgYWZ0ZXIgYSBoZWFkaW5nCiMgICAgICAgbWFya2VkLW1hbiB3aWxsIHJlbW92ZSBpdCBmcm9tIHRoZSBST0ZGIHZlcnNpb24uCiMgICAgIC0gVGhlIGZpcnN0IGhlYWRpbmcgbXVzdCBiZSBhIGxldmVsLTEgaGVhZGluZyBjb250YWluaW5nIHRoZSB1dGlsaXR5CiMgICAgICAgbmFtZSBhbmQgdmVyeSBicmllZiBkZXNjcmlwdGlvbjsgYXBwZW5kIHRoZSBtYW51YWwtc2VjdGlvbiBudW1iZXIKIyAgICAgICBkaXJlY3RseSB0byB0aGUgQ0xJIG5hbWU7IGUuZy46CiMgICAgICAgICAjIGZvbygxKSAtIGRvZXMgYmFyCiMgICAgIC0gVGhlIDJuZCwgbGV2ZWwtMiBoZWFkaW5nIG11c3QgYmUgJyMjIFNZTk9QU0lTJyBhbmQgdGhlIGNoYXB0ZXIncyBib2R5CiMgICAgICAgbXVzdCByZW5kZXIgcmVhc29uYWJseSBhcyBwbGFpbiB0ZXh0LCBiZWNhdXNlIGl0IGlzIHByaW50ZWQgdG8gc3Rkb3V0CiMgICAgICAgd2hlbiAgYC1oYCwgYC0taGVscGAgaXMgc3BlY2lmaWVkOgojICAgICAgICAgVXNlIDQtc3BhY2UgaW5kZW50YXRpb24gd2l0aG91dCBtYXJrdXAgZm9yIGJvdGggdGhlIHN5bnRheCBsaW5lIGFuZCB0aGUKIyAgICAgICAgIGJsb2NrIG9mIGJyaWVmIG9wdGlvbiBkZXNjcmlwdGlvbnM7IHJlcHJlc2VudCBvcHRpb24tYXJndW1lbnRzIGFuZCBvcGVyYW5kcwojICAgICAgICAgaW4gYW5nbGUgYnJhY2tldHM7IGUuZy4sICc8Zm9vPicKIyAgICAgLSBBbGwgb3RoZXIgaGVhZGluZ3Mgc2hvdWxkIGJlIGxldmVsLTIgaGVhZGluZ3MgaW4gQUxMLUNBUFMuCiMgICAtIFRFWFQKIyAgICAgIC0gVXNlIE5PIGluZGVudGF0aW9uIGZvciByZWd1bGFyIGNoYXB0ZXIgdGV4dDsgaWYgeW91IGRvLCBpdCB3aWxsCiMgICAgICAgIGJlIGluZGVudGVkIGZ1cnRoZXIgdGhhbiBsaXN0IGl0ZW1zLgojICAgICAgLSBVc2UgNC1zcGFjZSBpbmRlbnRhdGlvbiwgYXMgdXN1YWwsIGZvciBjb2RlIGJsb2Nrcy4KIyAgICAgIC0gTWFya3VwIGNoYXJhY3Rlci1zdHlsaW5nIG1hcmt1cCB0cmFuc2xhdGVzIHRvIFJPRkYgcmVuZGVyaW5nIGFzIGZvbGxvd3M6CiMgICAgICAgICBgLi4uYCBhbmQgKiouLi4qKiByZW5kZXIgYXMgYm9sZGVkIChyZWQpIHRleHQKIyAgICAgICAgIF8uLi5fIGFuZCAqLi4uKiByZW5kZXIgYXMgd29yZC1pbmRpdmlkdWFsbHkgdW5kZXJsaW5lZCB0ZXh0CiMgICAtIExJU1RTCiMgICAgICAtIEluZGVudCBsaXN0IGl0ZW1zIGJ5IDIgc3BhY2VzIGZvciBiZXR0ZXIgcGxhaW4tdGV4dCB2aWV3aW5nLCBidXQgbm90ZQojICAgICAgICB0aGF0IHRoZSBST0ZGIGdlbmVyYXRlZCBieSBtYXJrZWQtbWFuIHN0aWxsIHJlbmRlcnMgdGhlbSB1bmluZGVudGVkLgojICAgICAgLSBFbmQgZXZlcnkgbGlzdCBpdGVtIChidWxsZXQgcG9pbnQpIGl0c2VsZiB3aXRoIDIgdHJhaWxpbmcgc3BhY2VzIHRvbyBzbwojICAgICAgICB0aGF0IGl0IHJlbmRlcnMgb24gaXRzIG93biBsaW5lLgojICAgICAgLSBBdm9pZCBhc3NvY2lhdGluZyBtb3JlIHRoYW4gMSBwYXJhZ3JhcGggd2l0aCBhIGxpc3QgaXRlbSwgaWYgcG9zc2libGUsCiMgICAgICAgIGJlY2F1c2UgaXQgcmVxdWlyZXMgdGhlIGZvbGxvd2luZyB0cmljaywgd2hpY2ggaGFtcGVycyBwbGFpbi10ZXh0IHJlYWRhYmlsaXR5OgojICAgICAgICBVc2UgJyZuYnNwOzxzcGFjZT48c3BhY2U+JyBpbiBsaWV1IG9mIGFuIGVtcHR5IGxpbmUuCiMjIyMKOiA8PCdFT0ZfTUFOX1BBR0UnCiMgZmlsZWljb24oMSkgLSBtYW5hZ2UgZmlsZSBhbmQgZm9sZGVyIGN1c3RvbSBpY29ucwoKIyMgU1lOT1BTSVMKCk1hbmFnZSBjdXN0b20gaWNvbnMgZm9yIGZpbGVzIGFuZCBmb2xkZXJzIG9uIG1hY09TLiAgCgpTRVQgYSBjdXN0b20gaWNvbiBmb3IgYSBmaWxlIG9yIGZvbGRlcjoKCiAgICBmaWxlaWNvbiBzZXQgICAgICA8ZmlsZU9yRm9sZGVyPiBbPGltYWdlRmlsZT5dCgpSRU1PVkUgYSBjdXN0b20gaWNvbiBmcm9tIGEgZmlsZSBvciBmb2xkZXI6CgogICAgZmlsZWljb24gcm0gICAgICAgPGZpbGVPckZvbGRlcj4KCkdFVCBhIGZpbGUgb3IgZm9sZGVyJ3MgY3VzdG9tIGljb246CgogICAgZmlsZWljb24gZ2V0IFstZl0gPGZpbGVPckZvbGRlcj4gWzxpY29uT3V0cHV0RmlsZT5dCgogICAgLWYgLi4uIGZvcmNlIHJlcGxhY2VtZW50IG9mIGV4aXN0aW5nIG91dHB1dCBmaWxlCgpURVNUIGlmIGEgZmlsZSBvciBmb2xkZXIgaGFzIGEgY3VzdG9tIGljb246CgogICAgZmlsZWljb24gdGVzdCAgICAgPGZpbGVPckZvbGRlcj4KCkFsbCBmb3Jtczogb3B0aW9uIC1xIHNpbGVuY2VzIHN0YXR1cyBvdXRwdXQuCgpTdGFuZGFyZCBvcHRpb25zOiBgLS1oZWxwYCwgYC0tbWFuYCwgYC0tdmVyc2lvbmAsIGAtLWhvbWVgCgojIyBERVNDUklQVElPTgoKYDxmaWxlT3JGb2xkZXI+YCBpcyB0aGUgZmlsZSBvciBmb2xkZXIgd2hvc2UgY3VzdG9tIGljb24gc2hvdWxkIGJlIG1hbmFnZWQuICAKTm90ZSB0aGF0IHN5bWxpbmtzIGFyZSBmb2xsb3dlZCB0byB0aGVpciAodWx0aW1hdGUgdGFyZ2V0KTsgdGhhdCBpcywgeW91ICAKY2FuIG9ubHkgYXNzaWduIGN1c3RvbSBpY29ucyB0byByZWd1bGFyIGZpbGVzIGFuZCBmb2xkZXJzLCBub3QgdG8gc3ltbGlua3MgIAp0byB0aGVtLgoKYDxpbWFnZUZpbGU+YCBjYW4gYmUgYW4gaW1hZ2UgZmlsZSBvZiBhbnkgZm9ybWF0IHN1cHBvcnRlZCBieSB0aGUgc3lzdGVtLiAgCkl0IGlzIGNvbnZlcnRlZCB0byBhbiBpY29uIGFuZCBhc3NpZ25lZCB0byBgPGZpbGVPckZvbGRlcj5gLiAgCklmIHlvdSBvbWl0IGA8aW1hZ2VGaWxlPmAsIGA8ZmlsZU9yRm9sZGVyPmAgbXVzdCBpdHNlbGYgYmUgYW4gaW1hZ2UgZmlsZSB3aG9zZQppbWFnZSBzaG91bGQgYmVjb21lIGl0cyBvd24gaWNvbi4KCmA8aWNvbk91dHB1dEZpbGU+YCBzcGVjaWZpZXMgdGhlIGZpbGUgdG8gZXh0cmFjdCB0aGUgY3VzdG9tIGljb24gdG86ICAKRGVmYXVsdHMgdG8gdGhlIGZpbGVuYW1lIG9mIGA8ZmlsZU9yRm9sZGVyPmAgd2l0aCBleHRlbnNpb24gYC5pY25zYCBhcHBlbmRlZC4gIApJZiBhIHZhbHVlIGlzIHNwZWNpZmllZCwgZXh0ZW5zaW9uIGAuaWNuc2AgaXMgYXBwZW5kZWQsIHVubGVzcyBhbHJlYWR5IHByZXNlbnQuICAKRWl0aGVyIHdheSwgZXh0cmFjdGlvbiBmYWlscyBpZiB0aGUgdGFyZ2V0IGZpbGUgYWxyZWFkeSBleGlzdHM7IHVzZSBgLWZgIHRvICAKb3ZlcnJpZGUuICAKU3BlY2lmeSBgLWAgdG8gZXh0cmFjdCB0byBzdGRvdXQuICAKCkNvbW1hbmQgYHRlc3RgIHNpZ25hbHMgd2l0aCBpdHMgZXhpdCBjb2RlIHdoZXRoZXIgYSBjdXN0b20gaWNvbiBpcyBzZXQgKDApICAKb3Igbm90ICgxKTsgYW55IG90aGVyIGV4aXQgY29kZSBzaWduYWxzIGFuIHVuZXhwZWN0ZWQgZXJyb3IuCgoqKk9wdGlvbnMqKjoKCiAgKiBgLWZgLCBgLS1mb3JjZWAgIAogICAgV2hlbiBnZXR0aW5nIChleHRyYWN0aW5nKSBhIGN1c3RvbSBpY29uLCBmb3JjZXMgcmVwbGFjZW1lbnQgb2YgdGhlICAKICAgIG91dHB1dCBmaWxlLCBpZiBpdCBhbHJlYWR5IGV4aXN0cy4KCiAgKiBgLXFgLCBgLS1xdWlldGAgIAogICAgU3VwcHJlc3NlcyBvdXRwdXQgb2YgdGhlIHN0YXR1cyBpbmZvcm1hdGlvbiB0aGF0IGlzIGJ5IGRlZmF1bHQgb3V0cHV0IHRvICAKICAgIHN0ZG91dC4gIAogICAgTm90ZSB0aGF0IGVycm9ycyBhbmQgd2FybmluZ3MgYXJlIHN0aWxsIHByaW50ZWQgdG8gc3RkZXJyLgoKIyMgTk9URVMKCkN1c3RvbSBpY29ucyBhcmUgc3RvcmVkIGluIGV4dGVuZGVkIGF0dHJpYnV0ZXMgb2YgdGhlIEhGUysgZmlsZXN5c3RlbS4gIApUaHVzLCBpZiB5b3UgY29weSBmaWxlcyBvciBmb2xkZXJzIHRvIGEgZGlmZmVyZW50IGZpbGVzeXN0ZW0gdGhhdCBkb2Vzbid0ICAKc3VwcG9ydCBzdWNoIGF0dHJpYnV0ZXMsIGN1c3RvbSBpY29ucyBhcmUgbG9zdDsgZm9yIGluc3RhbmNlLCBjdXN0b20gaWNvbnMgIApjYW5ub3QgYmUgc3RvcmVkIGluIGEgR2l0IHJlcG9zaXRvcnkuCgpUbyBkZXRlcm1pbmUgaWYgYSBnaXZlIGZpbGUgb3IgZm9sZGVyIGhhcyBleHRlbmRlZCBhdHRyaWJ1dGVzLCB1c2UgIApgbHMgLWxAIDxmaWxlT3JGb2xkZXI+YC4KCldoZW4gc2V0dGluZyBhbiBpbWFnZSBhcyBhIGN1c3RvbSBpY29uLCBhIHNldCBvZiBpY29ucyB3aXRoIHNldmVyYWwgcmVzb2x1dGlvbnMgIAppcyBjcmVhdGVkLCB3aXRoIHRoZSBoaWdoZXN0IHJlc29sdXRpb24gYXQgNTEyIHggNTEyIHBpeGVscy4KCkFsbCBpY29ucyBjcmVhdGVkIGFyZSBzcXVhcmUsIHNvIGltYWdlcyB3aXRoIGEgbm9uLXNxdWFyZSBhc3BlY3QgcmF0aW8gd2lsbCAgCmFwcGVhciBkaXN0b3J0ZWQ7IGZvciBiZXN0IHJlc3VsdHMsIHVzZSBzcXVhcmUgaW1nZXMuCgojIyBTVEFOREFSRCBPUFRJT05TCgpBbGwgc3RhbmRhcmQgb3B0aW9ucyBwcm92aWRlIGluZm9ybWF0aW9uIG9ubHkuCgoqIGAtaCwgLS1oZWxwYCAgCiAgUHJpbnRzIHRoZSBjb250ZW50cyBvZiB0aGUgc3lub3BzaXMgY2hhcHRlciB0byBzdGRvdXQgZm9yIHF1aWNrIHJlZmVyZW5jZS4KCiogYC0tbWFuYCAgCiAgRGlzcGxheXMgdGhpcyBtYW51YWwgcGFnZSwgd2hpY2ggaXMgYSBoZWxwZnVsIGFsdGVybmF0aXZlIHRvIHVzaW5nIGBtYW5gLCAKICBpZiB0aGUgbWFudWFsIHBhZ2UgaXNuJ3QgaW5zdGFsbGVkLgoKKiBgLS12ZXJzaW9uYCAgCiAgUHJpbnRzIHZlcnNpb24gaW5mb3JtYXRpb24uCiAgCiogYC0taG9tZWAgIAogIE9wZW5zIHRoaXMgdXRpbGl0eSdzIGhvbWUgcGFnZSBpbiB0aGUgc3lzdGVtJ3MgZGVmYXVsdCB3ZWIgYnJvd3Nlci4KCiMjIExJQ0VOU0UKCkZvciBsaWNlbnNlIGluZm9ybWF0aW9uIGFuZCBtb3JlLCB2aXNpdCB0aGUgaG9tZSBwYWdlIGJ5IHJ1bm5pbmcgIApgZmlsZWljb24gLS1ob21lYAoKRU9GX01BTl9QQUdFCg=="


class Clown(Exception):
    pass


class CommandError(Clown):
    def __init__(self, message):
        sys.exit(message)


def command(cmd):
    out = subprocess.getstatusoutput(cmd)
    time.sleep(2)
    if out[0] == 0:
        return out[1]
    else:
        raise CommandError(f'Command Error: {out[1]}')


def python_version():
    version = str(command('python -V').split()[1][0])
    word = 'python'
    if version == '2':
        word = 'python3'
    return word


class MacSetup:
    def __init__(self):
        if os.path.isdir('mac_run'):
            print('Already ran mac_setup.py')
            return
        os.makedirs('mac_run')
        self.current_directory = os.getcwd()
        self.desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        self.python = python_version()
        self.make_command()
        self.make_fileicon()
        self.make_shortcut()
        self.cleanup()

    def make_command(self):
        with open('mac_run/d4d.command', 'w') as f:
            shebang = '#!/usr/bin/env bash'
            tellm = 'tell application "Terminal"'
            setm = 'set miniaturized of'
            window = '(first window whose name contains "d4d")'
            f.write(f'{shebang}\nosascript <<END_SCRIPT\n{tellm}\n{setm} {window} to true\nend tell\ndo shell script "cd {self.current_directory} && {self.python} dexcom4desktop.py"\n{tellm}\n{setm} {window} to false\nend tell\nEND_SCRIPT')
        time.sleep(0.2)
        command('chmod +x mac_run/d4d.command')

    def make_fileicon(self):
        base64_bytes = FILEICON.encode("ascii")
        string_bytes = base64.b64decode(base64_bytes)
        normal_string = string_bytes.decode("ascii")
        with open('fileicon', 'w') as f:
            f.write(normal_string)
        command('chmod +x fileicon')
        command('./fileicon set mac_run/d4d.command web/dexcom.png')

    def make_shortcut(self):
        command(f"""osascript -e 'tell application "Finder"' -e 'make new alias to file (posix file "{self.current_directory}/mac_run/d4d.command") at desktop' -e 'end tell'""")
        os.rename(f"{self.desktop}/d4d.command", f"{self.desktop}/d4d_alias.command")

    def cleanup(self):
        os.remove('fileicon')
        command(f"""osascript -e 'tell application "Finder"' -e 'move POSIX file "{self.desktop}/d4d_alias.command" to POSIX file "{self.current_directory}"' -e 'end tell'""")
        os.rename('d4d_alias.command', 'Dexcom 4 Desktop')


if __name__ == '__main__':
    MacSetup()
