import { Factory } from "miragejs"
import { faker } from "@faker-js/faker"

export const departamento = Factory.extend({
  description() {
    return faker.word.verb()
  },
})
