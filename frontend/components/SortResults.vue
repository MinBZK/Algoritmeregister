<template>
  <div class="sort">
    <div class="columns">
      <div class="column">
        Sorteer op:
        <ul class="sort__options">
          <li>
            <a
              href="#"
              role="button"
              class="sort--ascending is-active"
              aria-current="true"
              ><span class="visually-hidden">Sorteer op: </span>Datum<span
                class="visually-hidden"
              >
                oplopend</span
              ></a
            >
          </li>
          <li>
            <a
              href="#"
              role="button"
              class="sort--ascending"
              aria-current="false"
              ><span class="visually-hidden">Sorteer op: </span>Titel<span
                class="visually-hidden"
              >
                oplopend</span
              ></a
            >
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
