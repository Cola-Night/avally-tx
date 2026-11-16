from App.Module.MacroCSV import MacroCSV
from App.Module.Utility import *
from datetime import datetime, timezone
import uuid

# Testing "App/Module/MacroCSV"
def main() -> None:
  try:
    # Handler multiple CSV
    log = MacroCSV()

    # Create/Load CSV-File (input row=list)
    log.create(
      file='.temp/macro-csv-01.csv',
      name='EX01',
      headers=[
        'code',
        'name',
        'datetime',
      ],
    )

    # Create/Load CSV-File (input row=dict)
    log.create(
      file='.temp/macro-csv-02.csv',
      name='EX02',
      headers=[
        'code',
        'message',
      ],
    )
    
    # Get current DateTime (string/DateTime-UTC)
    dt = datetime.now(timezone.utc).isoformat()

    # Test append row with (list)
    log.append("EX01",[
      uuid.uuid4(),
      'append row with (list)',
      dt,
    ])

    # Test append row with (dict)
    log.append("EX02",{
      'code': uuid.uuid4(),
      'message': 'test dict 1',
    })

    # Test append row with (dict)
    log.append("EX02",{
      'code': uuid.uuid4(),
    })

    # Test append row with (dict)
    log.append("EX02",{
      'message': 'test dict 1',
    })

  except Exception as e:
    print(f"[ERROR] main: {e}")

# Start main function
if __name__ == "__main__":
  main()