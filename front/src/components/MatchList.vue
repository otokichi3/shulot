<template>
	<v-container>
		<v-row class="mt-6 text-center">
			<v-col cols="6" v-for="(match, index) in info" :key="match.id">
				<v-card class="light-green lighten-5 mx-auto" cols="12" max-width="400">
					<v-card-title class="subtitle-1 justify-center">
						{{ index + 1 }}コート
					</v-card-title>
					<v-divider></v-divider>
					<v-card-text>
						<v-row>
							<v-col cols="6" class="subtitle-2">{{ match.pair1.player1.name }}</v-col>
							<v-col cols="6" class="subtitle-2">{{ match.pair1.player2.name }}</v-col>
						</v-row>
						<v-row>
							<v-col class="caption">------- vs -------</v-col>
						</v-row>
						<v-row>
							<v-col cols="6" class="subtitle-2">{{ match.pair2.player1.name }}</v-col>
							<v-col cols="6" class="subtitle-2">{{ match.pair2.player2.name }}</v-col>
						</v-row>
					</v-card-text>
				</v-card>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import axios from 'axios';

export default {
	name: 'MatchList',

	data: () => ({
		info: null,
	}),
	mounted() {
		axios
			.get('http://localhost:8000')
			.then(res => (this.info = res.data.matchs))
			.catch((error) => console.log(error));
	},
}
</script>