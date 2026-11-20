from App.Module.MacroCSV import MacroCSV
from App.Module.Utility import *
from datetime import datetime, timezone
import uuid

# Testing "App/Module/MacroCSV"
def main() -> None:
  try:
    # Handler multiple CSV
    log = MacroCSV()

    # CSV save location
    save = '.temp/macro-csv-01.csv'

    # Create/Load CSV-File (input row=list)
    log.create(
      file=save,
      name='EX01',
      headers=[
        'code',
        'name',
        'note',
      ],
    )

    # Create CSV-Rows
    if False:

      # Insert CSV-Rows with (list)
      for i in range(10):
        no = str(i+1)
        z2 = no.zfill(2)
        z3 = no.zfill(3)
        z4 = no.zfill(4)

        # Insert CSV-Rows
        log.append('EX01',[
          f"L{z3}",
          f"Name-{z2}",
          f"Note-{z4}",
        ])

      # Insert CSV-Rows with (dict)
      for i in range(10):
        no = str(i+1)
        z2 = no.zfill(2)
        z3 = no.zfill(3)
        z4 = no.zfill(4)

        log.append('EX01',{
          'code': f"D{z3}",
          'name': f"Name-{z2}",
          'note': f"Note-{z4}",
        })

    # Select CSV-Rows
    records = log.getRecords('EX01', limit=4, skip=4)

    pp(records)

  except Exception as e:
    print(f"[ERROR] main: {e}")
