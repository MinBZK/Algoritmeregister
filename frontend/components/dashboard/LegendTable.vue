<template>
  <div :id="legendId" class="legend">
    <table class="legend-table">
      <tbody>
        <tr v-for="item in data" :key="item.title">
          <td class="legend-item">
            <div
              class="legend-item-shape"
              :style="{ backgroundColor: item.colour }"
            />
          </td>
          <td>
            {{ item.title }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  props: {
    data: {
      type: Array as () => { title: string; colour: string }[],
      default() {
        return []
      },
    },
    legendId: {
      type: String,
      default: '',
    },
  },
})
</script>

<style scoped lang="scss">
.legend-table {
  border: 0.1rem solid #e6e6e6;
  font-size: 14px;
  align-content: center;
}

.legend-item {
  align-content: center;
  width: 1em;
}

.legend-item-shape {
  height: 1rem;
  width: 1rem;
  border: 0.1rem solid grey;
}

@media (max-width: 768) {
  .legend-table {
    width: 40%;
  }
}
</style>
