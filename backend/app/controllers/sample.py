from fastapi import HTTPException

import services.sample as sample_services

class SampleController:
  def sample():
    sample = sample_services.get_sample()
    if not sample:
      raise HTTPException(500, "Failed to create sample")
    return sample