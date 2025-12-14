import { Injectable, HttpException } from '@nestjs/common';
import axios from 'axios';

@Injectable()
export class ValidateService {
  private FASTAPI_URL = 'http://127.0.0.1:8000/design/validate';

  async validate(text: string) {
    try {
      const response = await axios.post(this.FASTAPI_URL, { text });
      return response.data; 
    } catch (error: any) {
      console.error('FastAPI error:', error?.message);
      if (error?.response) {
        console.error('FastAPI response:', error.response.data);
      }
      throw new HttpException('Validation service failed', 500);
    }
  }
}
