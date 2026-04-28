devtools::install_github("saberpowers/sabRmetrics")     # You don't need to run this line every time

new_data <- sabRmetrics::download_statsapi(start_date = "2026-02-20", end_date = "2026-04-14")

new_data$pitch |>
  dplyr::filter(abs_challenged) |>
  dplyr::select(game_id, play_id, event_index, abs_overturned, abs_team_id, abs_player_id, dplyr::everything())


# New data to csv on all pitches regardless of challenge
new_data$pitch |>
  readr::write_csv("data/pitch_data_2026.csv")