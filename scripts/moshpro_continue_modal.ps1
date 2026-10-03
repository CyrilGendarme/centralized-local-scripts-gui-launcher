param([string]$Message = "foo")
Add-Type -AssemblyName System.Windows.Forms
$form = New-Object System.Windows.Forms.Form
$form.Text = "Mosh-Pro"
$form.Size = New-Object System.Drawing.Size(380, 180)
$form.StartPosition = "CenterScreen"
$form.TopMost = $true
$form.FormBorderStyle = "FixedDialog"
$form.MaximizeBox = $false
$form.MinimizeBox = $false
$label = New-Object System.Windows.Forms.Label
$label.Text = $Message
$label.AutoSize = $false
$label.Size = New-Object System.Drawing.Size(340, 60)
$label.Location = New-Object System.Drawing.Point(15, 15)
$button = New-Object System.Windows.Forms.Button
$button.Text = "Continue"
$button.Size = New-Object System.Drawing.Size(100, 30)
$button.Location = New-Object System.Drawing.Point(140, 90)
$button.DialogResult = [System.Windows.Forms.DialogResult]::OK
$form.AcceptButton = $button
$form.Controls.AddRange(@($label, $button))
[void]$form.ShowDialog()