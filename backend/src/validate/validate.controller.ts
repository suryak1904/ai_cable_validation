import { Controller, Post, Body } from '@nestjs/common';
import { ValidateService } from './validate.service';
import { ValidateDto } from './validate.dto';

@Controller('validate')
export class ValidateController {
  constructor(private readonly service: ValidateService) {}

  @Post()
  async validate(@Body() dto: ValidateDto) {
    return this.service.validate(dto.text);
  }
}
